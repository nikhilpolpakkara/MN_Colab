from historical_timelines import HistoricalTimeline

timeline = HistoricalTimeline("Timeline from my csv")
timeline_json = HistoricalTimeline.json_from_csv(
    "timeline.csv",
    "ï»¿Name",
    "Description",
    "Label",
    "Start",
    "End",
)

timeline.populate_timeline_from_dict(timeline_json)
timeline.render_timeline("timeline.html")