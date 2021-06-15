from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    #########  reading  #########
    @staticmethod
    def read_history():
        sql = 'SELECT HistoryID, ActionDate, Value, Name, Action.Description FROM History INNER JOIN Action ON History.ActionID = Action.ActionID INNER JOIN Devices ON History.DeviceID = Devices.DeviceID ORDER BY ActionDate desc'
        return Database.get_rows(sql)

    def read_devices():
        sql = 'SELECT DeviceID, Name, Description, Type, COALESCE(MinValue, \'\') as `MinValue`, COALESCE(Devices.MaxValue, \'\') as `MaxValue`, COALESCE(Unit, \'\') as `Unit` FROM Devices;'
        return Database.get_rows(sql)


    #########  logging  #########
    @staticmethod
    def create_log_moist(date, value, deviceID='MOIST', actionID=5):
        sql = "INSERT INTO History(ActionDate, Value, DeviceID, ActionID) VALUES(%s,%s,%s,%s)"
        params = [date, value, deviceID, actionID]
        return Database.execute_sql(sql, params)

    @staticmethod
    def create_log_VIS(date, value, deviceID='SUNVIS', actionID=8):
        sql = "INSERT INTO History(ActionDate, Value, DeviceID, ActionID) VALUES(%s,%s,%s,%s)"
        params = [date, value, deviceID, actionID]
        return Database.execute_sql(sql, params)

    @staticmethod
    def create_log_UV(date, value, deviceID='SUNUV', actionID=7):
        sql = "INSERT INTO History(ActionDate, Value, DeviceID, ActionID) VALUES(%s,%s,%s,%s)"
        params = [date, value, deviceID, actionID]
        return Database.execute_sql(sql, params)

    @staticmethod
    def create_log_IR(date, value, deviceID='SUNIR', actionID=4):
        sql = "INSERT INTO History(ActionDate, Value, DeviceID, ActionID) VALUES(%s,%s,%s,%s)"
        params = [date, value, deviceID, actionID]
        return Database.execute_sql(sql, params)

    @staticmethod
    def create_log_temp(date, value, deviceID='TEMP', actionID=2):
        sql = "INSERT INTO History(ActionDate, Value, DeviceID, ActionID) VALUES(%s,%s,%s,%s)"
        params = [date, value, deviceID, actionID]
        return Database.execute_sql(sql, params)

    @staticmethod
    def create_log_humi(date, value, deviceID='HUM', actionID=3):
        sql = "INSERT INTO History(ActionDate, Value, DeviceID, ActionID) VALUES(%s,%s,%s,%s)"
        params = [date, value, deviceID, actionID]
        return Database.execute_sql(sql, params)

    @staticmethod
    def create_log_air(date, value, deviceID='AIR', actionID=6):
        sql = "INSERT INTO History(ActionDate, Value, DeviceID, ActionID) VALUES(%s,%s,%s,%s)"
        params = [date, value, deviceID, actionID]
        return Database.execute_sql(sql, params)

    @staticmethod
    def create_log_actuator(date, value, deviceID, actionID=1):
        sql = "INSERT INTO History(ActionDate, Value, DeviceID, ActionID) VALUES(%s,%s,%s,%s)"
        params = [date, value, deviceID, actionID]
        return Database.execute_sql(sql, params)