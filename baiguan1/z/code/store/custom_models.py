from custom_model.base import CustomModel


class OverallOnlineRank(CustomModel):

    class Meta:
        table_name = 'online_items_score_overall'


class DailyOnlineRank(CustomModel):

    class Meta:
        table_name = 'online_items_score_daily'


class WeeklyOnlineRank(CustomModel):

    class Meta:
        table_name = 'online_items_score_weekly'


class MonthlyOnlineRank(CustomModel):

    class Meta:
        table_name = 'online_items_score_monthly'
