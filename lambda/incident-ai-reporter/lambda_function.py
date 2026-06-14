import json, boto3, os, time
from datetime import datetime, timezone

athena     = boto3.client('athena')
comprehend = boto3.client('comprehend', region_name='ap-south-1')
sns        = boto3.client('sns')

BUCKET  = os.environ['BUCKET_NAME']
SNS_ARN = os.environ['SNS_ARN']

def lambda_handler(event, context):
    query = """
        SELECT
            incident_type,
            stop_code,
            COUNT(*) as total_count,
            COUNT(CASE WHEN timestamp >= date_format(current_timestamp - interval '1' day, '%Y-%m-%dT%H:%i:%s') THEN 1 END) as last_24h,
            COUNT(CASE WHEN timestamp >= date_format(current_timestamp - interval '7' day, '%Y-%m-%dT%H:%i:%s') THEN 1 END) as last_7_days,
            MAX(timestamp) as last_seen
        FROM incident_db.incidents
        GROUP BY incident_type, stop_code
        ORDER BY total_count DESC
        LIMIT 10
    """
    result = run_athena_query(query)
    rows   = json.loads(result)

    summary_lines   = []
    incident_counts = {}
    trend_data      = {}

    for row in rows[1:]:
        cols = [c.get('VarCharValue', '0') for c in row['Data']]
        if len(cols) >= 6:
            incident_type = cols[0]
            stop_code     = cols[1]
            total         = int(cols[2]) if cols[2].isdigit() else 0
            last_24h      = int(cols[3]) if cols[3].isdigit() else 0
            last_7d       = int(cols[4]) if cols[4].isdigit() else 0
            last_seen     = cols[5]

            summary_lines.append({
                "type":      incident_type,
                "code":      stop_code,
                "total":     total,
                "last_24h":  last_24h,
                "last_7d":   last_7d,
                "last_seen": last_seen
            })
            incident_counts[incident_type] = total
            trend_data[incident_type] = {
                "last_24h": last_24h,
                "last_7d":  last_7d
            }

    incident_text = (
        "ECS incidents: " + ", ".join([f"{s['type']} x{s['total']}" for s in summary_lines])
        if summary_lines else "No incidents detected in ECS cluster."
    )
    if len(incident_text.encode('utf-8')) > 4900:
        incident_text = incident_text[:4900]

    sentiment_response = comprehend.detect_sentiment(
        Text=incident_text,
        LanguageCode='en'
    )
    sentiment = sentiment_response['Sentiment']
    scores    = sentiment_response['SentimentScore']

    report = generate_report(
        incident_counts, trend_data, sentiment, scores, summary_lines
    )

    now_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    sns.publish(
        TopicArn=SNS_ARN,
        Subject=f"[INCIDENT REPORT] AWS ECS Fargate | {now_date} | ap-south-1",
        Message=report
    )
    return {"statusCode": 200, "body": report}


def generate_report(incident_counts, trend_data, sentiment, scores, summary_lines):
    total     = sum(incident_counts.values())
    total_24h = sum(t['last_24h'] for t in trend_data.values())
    total_7d  = sum(t['last_7d']  for t in trend_data.values())
    now       = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # Risk Level
    if total == 0:
        risk      = "LOW"
        risk_tag  = "[ OK ]"
        risk_note = "No incidents detected. Infrastructure is operating normally."
    elif total_24h >= 5 or total >= 15:
        risk      = "HIGH"
        risk_tag  = "[ HIGH ]"
        risk_note = "High incident frequency detected. Immediate investigation required."
    elif total_24h >= 2 or total >= 7:
        risk      = "MEDIUM"
        risk_tag  = "[ MEDIUM ]"
        risk_note = "Elevated incident rate. Engineering review recommended within 24 hours."
    else:
        risk      = "LOW-MEDIUM"
        risk_tag  = "[ LOW-MEDIUM ]"
        risk_note = "Minor incidents detected. Monitor closely over the next 24 hours."

    # Trend
    if total == 0:
        trend = "STABLE     | No incidents recorded in the monitoring window."
    elif total_24h > total_7d * 0.5:
        trend = "ESCALATING | Incident rate is increasing. Investigate immediately."
    elif total_24h == 0 and total_7d > 0:
        trend = "RECOVERING | No incidents in last 24h. System appears to be stabilizing."
    else:
        trend = "STABLE     | Incident rate is within normal operational bounds."

    # Sentiment
    sentiment_map = {
        "POSITIVE": "POSITIVE | Infrastructure patterns appear healthy.",
        "NEGATIVE": "NEGATIVE | Anomalous patterns detected in incident data.",
        "NEUTRAL":  "NEUTRAL  | Normal operational variance observed.",
        "MIXED":    "MIXED    | Conflicting signals detected in incident data."
    }
    sentiment_label = sentiment_map.get(sentiment, sentiment)

    # Root Causes
    root_causes = {
        "CONTAINER_CRASH": [
            "Application process exited unexpectedly inside the container.",
            "Triggers : Unhandled exceptions, segmentation faults, missing",
            "           runtime dependencies, or misconfigured env variables."
        ],
        "STARTUP_FAILURE": [
            "ECS task failed before the container became healthy.",
            "Triggers : Invalid ECR image URI, IAM permission gaps on the",
            "           task execution role, or ECR network connectivity failure."
        ],
        "OOM_KILL": [
            "Container was forcibly terminated by the Linux OOM killer.",
            "Triggers : Memory consumption exceeded the task-level limit.",
            "           Possible causes: memory leaks or under-provisioned memory."
        ],
        "MANUAL_STOP": [
            "Task was intentionally stopped via API, console, or pipeline.",
            "Note     : Expected behavior during rolling deployments.",
            "           This does not indicate a system fault."
        ],
        "UNKNOWN": [
            "ECS did not provide a specific stop code for this task.",
            "Triggers : Container runtime crashed before reporting exit status.",
            "           Inspect CloudWatch Logs for the specific task ARN."
        ]
    }

    # Recommendations
    priority  = 1
    rec_lines = []
    if "OOM_KILL" in incident_counts:
        rec_lines += [
            f"  P{priority} | SEVERITY : HIGH",
            f"     Action    : Increase memory allocation in the ECS task definition.",
            f"     Detail    : Memory threshold is being consistently exceeded.",
            f"     Follow-up : Profile heap usage and audit application for memory leaks.",
            ""
        ]
        priority += 1
    if "CONTAINER_CRASH" in incident_counts:
        rec_lines += [
            f"  P{priority} | SEVERITY : HIGH",
            f"     Action    : Review CloudWatch Logs for crashed container exit codes.",
            f"     Detail    : Identify the root exception causing the process to exit.",
            f"     Follow-up : Add retry logic and graceful shutdown handlers.",
            ""
        ]
        priority += 1
    if "STARTUP_FAILURE" in incident_counts:
        rec_lines += [
            f"  P{priority} | SEVERITY : MEDIUM",
            f"     Action    : Verify ECR image URI and confirm NAT Gateway routing.",
            f"     Detail    : Tasks are failing before reaching a running state.",
            f"     Follow-up : Audit task execution IAM role for ECR pull permissions.",
            ""
        ]
        priority += 1
    if "UNKNOWN" in incident_counts:
        rec_lines += [
            f"  P{priority} | SEVERITY : MEDIUM",
            f"     Action    : Enable awslogs driver in the ECS task definition.",
            f"     Detail    : Stop reason is undetermined — improve observability.",
            f"     Follow-up : Review raw task stop events in the ECS console.",
            ""
        ]
        priority += 1
    if "MANUAL_STOP" in incident_counts:
        rec_lines += [
            f"  P{priority} | SEVERITY : LOW",
            f"     Action    : Confirm all manual stops were authorized actions.",
            f"     Detail    : Manual stops are expected during deployments.",
            f"     Follow-up : Cross-reference with deployment and release logs.",
            ""
        ]
        priority += 1
    if not rec_lines:
        rec_lines = [
            "  No immediate actions required. Continue standard monitoring cadence."
        ]

    # Incident Table
    header   = f"  {'INCIDENT TYPE':<22}  {'TOTAL':>7}  {'24H':>6}  {'7D':>6}  {'STATUS':<10}  LAST SEEN"
    divider  = "  " + "-" * 74
    rows_out = []
    for s in summary_lines:
        status = (
            "[ACTIVE]" if s['last_24h'] > 0
            else "[RECENT]" if s['last_7d'] > 0
            else "[OLDER] "
        )
        rows_out.append(
            f"  {s['type']:<22}  {s['total']:>7}  {s['last_24h']:>6}  "
            f"{s['last_7d']:>6}  {status:<10}  {s['last_seen'][:19]}"
        )
    if not rows_out:
        rows_out = ["  No incidents found in the monitoring window."]

    # Root Cause Block
    rc_block = []
    for idx, (itype, count) in enumerate(incident_counts.items(), 1):
        lines = root_causes.get(itype, ["Review CloudWatch Logs for this task ARN."])
        occ   = f"occurrence{'s' if count != 1 else ''}"
        rc_block.append(f"  {idx}.  {itype}  ({count} {occ})")
        for line in lines:
            rc_block.append(f"       {line}")
        rc_block.append("")
    if not rc_block:
        rc_block = ["  No incidents to analyze."]

    # NLP Score Bars
    pos_bar = round(scores['Positive'] * 20)
    neg_bar = round(scores['Negative'] * 20)
    neu_bar = round(scores['Neutral']  * 20)

    D = "=" * 66
    S = "-" * 66

    report = f"""\
{D}
  CLOUD INCIDENT INTELLIGENCE REPORT
  AWS ECS Fargate  |  Region: ap-south-1
  Report Generated : {now}
{D}

EXECUTIVE SUMMARY
{S}
  Risk Level      : {risk_tag} {risk}
  Assessment      : {risk_note}
  Incident Trend  : {trend}
  Health Signal   : {sentiment_label}

{S}
INCIDENT METRICS
{S}
  Total Incidents (all time)   : {total}
  Incidents in Last 24 Hours   : {total_24h}
  Incidents in Last 7 Days     : {total_7d}
  Unique Incident Types        : {len(incident_counts)}

  Health Score Breakdown (Amazon Comprehend NLP)
  Positive : {scores['Positive']:>5.1%}  {"#" * pos_bar}
  Negative : {scores['Negative']:>5.1%}  {"#" * neg_bar}
  Neutral  : {scores['Neutral']:>5.1%}  {"#" * neu_bar}
  Mixed    : {scores['Mixed']:>5.1%}

{S}
INCIDENT BREAKDOWN
{S}
{header}
{divider}
{chr(10).join(rows_out)}

{S}
ROOT CAUSE ANALYSIS
{S}
{chr(10).join(rc_block)}
{S}
PRIORITIZED RECOMMENDATIONS
{S}
{chr(10).join(rec_lines)}
{S}
INFRASTRUCTURE STATUS
{S}
  Cluster          : incident-intel-cluster
  Region           : ap-south-1
  Desired Tasks    : 2     Auto-Scaling   : 1 min / 4 max tasks
  CPU Threshold    : 50%   Self-Healing   : ENABLED
  Monitoring       : Amazon CloudWatch + Amazon Athena
  AI Engine        : Amazon Comprehend (NLP Sentiment Analysis)
  Data Warehouse   : Amazon S3 + Amazon Athena
  Alert Channel    : Amazon SNS (Email)

{D}
  Powered by Amazon Comprehend | Athena | ECS Fargate | Lambda
  This report is system-generated. Do not reply to this email.
{D}"""

    return report


def run_athena_query(query):
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': 'incident_db'},
        ResultConfiguration={
            'OutputLocation': f's3://{BUCKET}/athena-results/'
        }
    )
    exec_id = response['QueryExecutionId']
    while True:
        status = athena.get_query_execution(QueryExecutionId=exec_id)
        state  = status['QueryExecution']['Status']['State']
        if state in ['SUCCEEDED', 'FAILED']:
            break
        time.sleep(2)
    results = athena.get_query_results(QueryExecutionId=exec_id)
    return json.dumps(results['ResultSet']['Rows'], indent=2)
