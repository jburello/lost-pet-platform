from backend.app.pet_report import PetReport, ReportType

class ReportManager:

    def __init__(self):
        self.reports = {}


    def add_report(self,pet_report):
        self.reports[pet_report.report_id] = pet_report

    def get_report_by_id(self, report_id):
        return self.reports.get(report_id)

    def get_all_reports(self):
        return list(self.reports.values())

    def filter_by_report_type(self,report_type):
        list_of_reports = []
        for report in self.reports.values():
            if report_type == report.report_type:
                list_of_reports.append(report)
        return list_of_reports

    def delete_report(self, report_id):
        self.reports.pop(report_id, None)

    def update_report(self, report_id, updates):
        report = self.get_report_by_id(report_id)
        for field, value in updates.items():
            setattr(report,field,value)
        return report