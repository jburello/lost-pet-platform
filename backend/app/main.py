from pet_report import PetReport, ReportType


lost_report = PetReport(
    ReportType.LOST,
    "dog",
    "The Woodlands, TX",
    "Black and white husky wearing a red collar.",
    "2026-08-10 18:30",
    name="Milo",
    breed="Husky",
    sex="male",
    color="black and white"
)

found_report = PetReport(
    ReportType.FOUND,
    "cat",
    "Conroe, TX",
    "Small orange cat found near an apartment complex.",
    "2026-08-10 19:15",
    sex="female",
    color="orange"
)

sighting_report = PetReport(
    ReportType.SIGHTING,
    "dog",
    "Oak Ridge North, TX",
    "Saw a medium-sized dog running near the road. Could not get close enough to identify the breed.",
    "2026-08-10 20:05",
    color="brown"
)


reports = [
    lost_report,
    found_report,
    sighting_report
]

for report in reports:
    print(report.report_id)
    print(report.report_type)
    print(report.name)
    print()