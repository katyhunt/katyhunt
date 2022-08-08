"""
Created on Fri Jun 17 1:59:00 2022

@author: katyhunt
"""
import datetime
from astropy.time import Time
from sgp4.io import fix_checksum


class TLE(object):
    """
    instance attributes:
        "name" (String)
            max 24 characters
        "sat_num" (int)
            satellite number, max 5 characters
        "classification" (String)
            1 character
        "int_designator" (String)
            international designator, max 8 characters
        "epoch_year" (int)
            last two digits of Gregorian year
        "epoch_day" (float)
            Julian day and fractional portion of the day from time
        "mm_deriv1" (float)
            first derivative of mean motion, always less than one
            (if you want a first derivative greater than one, you must manually input in text file)
        "mm_deriv2" (String or 0)
            second derivative of mean motion, decimal point assumed
        "B" (String or 0)
            drag term aka radiation pressure coefficient, decimal point assumed
        "set_num" (int)
            element set number, incremented when a new TLE is generated for this object
        "check_sum2" and "check_sum3"
            one for both the second and third lines, begins at zero,
            adds a value of each digit in the line, adds one for each minus sign
            and two for each plus sign, and takes the last decimal digit of the result as the check sum
        "inclination" (float)
            in degrees
        "right_asc_node" (float)
            right ascension of the ascending node, in degrees
        "eccentricity" (float)
            decimal point assumed
        "arg_perigee" (flfile_nameons per day
        "rev_num" (int)
            revolution number at epoch, in revolutions
    default attributes:
        Satellite named "No_Name" on January 1st, 2022
        Inclination and right ascension are both set to 30.0 degrees
        Eccentricity is set to 0.0005
        Mean motion is set to 1.0
        Element set number is set to 1
        Every other attribute is set to 0
    parameters:
        no needed parameters
        name, sat_num, classification, int_designator, mm_deriv1,
            mm_deriv2, B, inclination, right_asc_node, eccentricity,
            arg_perigee, mean_anomaly, mean_motion, and rev_num
            can be inputted as parameters
    public methods:
        set_date_time()
            sets epoch_year and epoch_day based on the inputted date_time
            inputs: date_time (date_time object from datetime library)
            outputs: none
        set_date_to_today()
            sets epoch_year and epoch_day based on today's date_time
            inputs: none
            outputs: none
        to_str()
            returns TLE in the form of a string that can be printed with correct formatting
            inputs: none
            outputs: string
        to_txt()
            If a file exists under the inputted name, that file is opened,
                and the current text is replaced with the TLE
            If a file doesn't exist yet under the inputted name,
                that file is created and the TLE is written into it
            inputs: file_name (String)
            outputs: text_file (.txt file)
        append_to_txt()
            file is opened under the name inputted,
            existing lines in the file are read in,
            the tle lines are appended to the existing lines,
            and all the lines, existing and new, are written into the file
            inputs: file_name (String)
            outputs: text_file (.txt file)
        create_tle_from_txt(file_name)
            the file under file_name is read in
            a TLE object is created with those parameters
                (assumes the text file has correct formatting)
            print_params() is called
            inputs: file_name (String)
            outputs: none
        create_tle_from_str(input_str)
            a TLE object is created with the string's parameters
                (assumes the string has correct formatting and \n for each of the three TLE lines)
            print_params() is called
            inputs: input_str (String)
            outputs: none
        print_params()
            all parameters of the TLE object are printed
            inputs: none
            outputs:none
        ISS()
            sets all the parameters of the tle to those of the International Space Station (ISS)
            inputs: none
            outputs: none
    private methods:
        __gen_tle - formats TLE, called in initialization,
                    set_date_time(), set_date_to_today(), and ISS()
    """

    def __init__(
        self,
        name="Satellite",
        sat_num=0,
        classification="U",
        int_designator="000000",
        epoch_year=22,
        epoch_day=1,
        mm_deriv1=0,
        mm_deriv2=0,
        B=0,
        inclination=30.0,
        right_asc_node=0.0,
        eccentricity=0.0006703,
        arg_perigee=130.5360,
        mean_anomaly=0,
        mean_motion=1,
        rev_num=00000,
        set_num=1,
    ):
        self.__gen_tle(
            name,
            sat_num,
            classification,
            int_designator,
            epoch_year,
            epoch_day,
            mm_deriv1,
            mm_deriv2,
            B,
            inclination,
            right_asc_node,
            eccentricity,
            arg_perigee,
            mean_anomaly,
            mean_motion,
            rev_num,
            set_num,
        )

    def __gen_tle(
        self,
        name,
        sat_num,
        classification,
        int_designator,
        epoch_year,
        epoch_day,
        mm_deriv1,
        mm_deriv2,
        B,
        inclination,
        right_asc_node,
        eccentricity,
        arg_perigee,
        mean_anomaly,
        mean_motion,
        rev_num,
        set_num,
    ):
        # setting attributes
        self.name = name
        self.sat_num = sat_num
        self.classification = classification
        self.int_designator = int_designator
        self.epoch_year = epoch_year
        self.epoch_day = epoch_day
        self.mm_deriv1 = mm_deriv1
        if mm_deriv2 == 0:
            self.mm_deriv2 = " 00000-0"
        else:
            self.mm_deriv2 = mm_deriv2
        if B == 0:
            self.B = " 00000-0"
        else:
            self.B = B
        self.set_num = set_num
        self.inclination = inclination
        self.right_asc_node = right_asc_node
        self.eccentricity = eccentricity
        self.arg_perigee = arg_perigee
        self.mean_anomaly = mean_anomaly
        self.mean_motion = mean_motion
        self.rev_num = rev_num
        self.lines = []

        # raising exceptions for incorrect parameters
        if not isinstance(self.sat_num, int) and not isinstance(self.sat_num, float):
            raise Exception("sat_num (satellite number) must be an integer")
        if not isinstance(self.classification, str):
            raise Exception("classification must be a string")
        if not isinstance(self.int_designator, str):
            raise Exception(
                "int_designator (international designator) must be a string"
            )
        if not isinstance(self.epoch_year, int) and not isinstance(
            self.epoch_year, float
        ):
            raise Exception("epoch_year must be an integer")
        if not isinstance(self.epoch_day, int) and not isinstance(
            self.epoch_day, float
        ):
            raise Exception("epoch_day must be a float")
        if not isinstance(self.mm_deriv1, int) and not isinstance(
            self.mm_deriv1, float
        ):
            raise Exception("mm_deriv1 must be a float")
        if not isinstance(self.mm_deriv2, str) and self.mm_deriv2 != 0:
            raise Exception("mm_deriv2 must be a string in the form '(-)XXXXX-X'")
        if isinstance(self.mm_deriv2, str) and str(self.mm_deriv2)[-2] != "-":
            raise Exception("Please input mm_deriv2 in the form '(-)XXXXX-X'")
        if not isinstance(self.B, str) and self.B != 0:
            raise Exception("B (drag term) must be a string in the form '(-)XXXXX-X'")
        if isinstance(self.B, str) and str(self.B)[-2] != "-":
            raise Exception("Please input B (drag term) in the form '(-)XXXXX-X'")
        if not isinstance(self.set_num, int) and not isinstance(self.set_num, float):
            raise Exception("set_num (element set number) must be an integer")
        if not isinstance(self.inclination, int) and not isinstance(
            self.inclination, float
        ):
            raise Exception("inclination must be a float")
        if not isinstance(self.right_asc_node, int) and not isinstance(
            self.right_asc_node, float
        ):
            raise Exception("right_asc_node must be a float")
        if not isinstance(self.eccentricity, int) and not isinstance(
            self.eccentricity, float
        ):
            raise Exception("eccentricity must be a float")
        if not isinstance(self.arg_perigee, int) and not isinstance(
            self.arg_perigee, float
        ):
            raise Exception("arg_perigee (argument of perigee) must be a float")
        if not isinstance(self.mean_anomaly, int) and not isinstance(
            self.mean_anomaly, float
        ):
            raise Exception("mean_anomaly must be a float")
        if not isinstance(self.mean_motion, int) and not isinstance(
            self.mean_motion, float
        ):
            raise Exception("mean_motion must be a float")
        if not isinstance(self.rev_num, int) and not isinstance(self.rev_num, float):
            raise Exception("rev_num (revolution number at epoch) must be an integer")
        if self.epoch_year > 99 or self.epoch_day > 366:
            raise Exception("That is not a feasible date.")
        if len(self.classification) != 1:
            raise Exception(
                "Classification must be 1 character: 'U' for unclassified, 'C' for classified, or 'S' for secret"
            )

        # determining the sign of mm_deriv1 (needed for formatting)
        if int(self.mm_deriv1) < 0:
            mm1_sign = "-"
        else:
            mm1_sign = " "

        # writing name line (line[0])
        self.lines.append("{0:24s}".format(str(self.name)))

        self.lines.append(
            "1 {0:05d}{1:1s} {2:8s} {3:02d}{4:0<12f} {5}.{6} {7:>7} {8:>7} 0 {9:4}".format(
                int(self.sat_num),
                self.classification,
                self.int_designator,
                int(self.epoch_year),
                float(self.epoch_day),
                mm1_sign,
                "{0:.8f}".format(float(self.mm_deriv1)).split(".")[1],
                str(self.mm_deriv2),
                str(self.B),
                int(self.set_num),
            )
        )

        # writing line 2 (lines[2])
        self.lines.append(
            "2 {0:05d} {1:8.4f} {2:8.4f} {3} {4:8.4f} {5:8.4f} {6:0<11f}{7:05d}".format(
                int(self.sat_num),
                float(self.inclination),
                float(self.right_asc_node),
                "{0:.7f}".format(float(self.eccentricity)).split(".")[1],
                float(self.arg_perigee),
                float(self.mean_anomaly),
                float(self.mean_motion),
                int(self.rev_num),
            )
        )

        # finding checksum and updating lines
        self.lines[1] = fix_checksum(self.lines[1])
        self.lines[2] = fix_checksum(self.lines[2])

    def set_date_time(self, date_time):
        """
        sets epoch_year and epoch_day based on the inputted date_time
        inputs: date_time (date_time object)
        outputs: none
        """
        dt = [float(dt) for dt in Time(date_time).yday.split(":")]
        self.epoch_year = int(dt[0] - 2000)
        self.epoch_day = dt[1] + dt[2] / 24 + dt[3] / 1440 + dt[4] / 86400

        self.__gen_tle(
            self.name,
            self.sat_num,
            self.classification,
            self.int_designator,
            self.epoch_year,
            self.epoch_day,
            self.mm_deriv1,
            self.mm_deriv2,
            self.B,
            self.inclination,
            self.right_asc_node,
            self.eccentricity,
            self.arg_perigee,
            self.mean_anomaly,
            self.mean_motion,
            self.rev_num,
            self.set_num,
        )
        return

    def set_date_to_today(self):
        """
        sets epoch_year and epoch_day based on today's date_time
        inputs: none
        outputs: none
        """
        dt = [float(dt) for dt in Time(datetime.datetime.today()).yday.split(":")]
        self.epoch_year = int(dt[0] - 2000)
        self.epoch_day = dt[1] + dt[2] / 24 + dt[3] / 1440 + dt[4] / 86400

        self.__gen_tle(
            self.name,
            self.sat_num,
            self.classification,
            self.int_designator,
            self.epoch_year,
            self.epoch_day,
            self.mm_deriv1,
            self.mm_deriv2,
            self.B,
            self.inclination,
            self.right_asc_node,
            self.eccentricity,
            self.arg_perigee,
            self.mean_anomaly,
            self.mean_motion,
            self.rev_num,
            self.set_num,
        )
        return

    def to_str(self):
        """
        returns TLE in the form of a string that can be printed with correct formatting
        inputs: none
        outputs: string
        """
        return self.lines[0] + "\n" + self.lines[1] + "\n" + self.lines[2]

    def to_txt(self, file_name):
        """
        If a file exists under the inputted name, that file is opened,
            and the current text is replaced with the TLE
        If a file doesn't exist yet under the inputted name,
            that file is created and the TLE is written into it
        inputs: file_name (String)
        outputs: text_file (.txt file)
        """
        with open(file_name, "w") as text_file:
            text_file.writelines("\n".join(self.lines))
        return text_file

    def append_to_txt(self, file_name):
        """
        file is opened under the name inputted,
            existing lines in the file are read in,
            the tle lines are appended to the existing lines,
            and all the lines, existing and new, are written into the file
        inputs: file_name (String)
        outputs: text_file (.txt file)
        """
        with open(file_name, "r") as text_file:
            existing_lines = text_file.readlines()

        append_lines = []
        for line in existing_lines:
            append_lines.append(line)
        append_lines.append("\n" + self.lines[0])
        append_lines.append("\n" + self.lines[1])
        append_lines.append("\n" + self.lines[2])
        with open(file_name, "w") as text_file:
            for new_line in append_lines:
                text_file.write(new_line)
        return text_file

    def create_tle_from_txt(self, file_name):
        """
        the file under file_name is read in
        a TLE object is created with those parameters
            (assumes the text file has correct formatting)
        print_params() is called
        inputs: file_name (String)
        outputs: none
        """
        with open(file_name, "r") as text_file:
            lines = text_file.readlines()

        self.__gen_tle(
            name=lines[0].rstrip(),
            sat_num=int(lines[1][2:7]),
            classification=lines[1][7],
            int_designator=lines[1][9:17],
            epoch_year=int(lines[1][18:20]),
            epoch_day=float(lines[1][20:32]),
            mm_deriv1=float(lines[1][33] + "0" + lines[1][34:43]),
            mm_deriv2=lines[1][44:52],
            B=lines[1][53:61],
            set_num=int(lines[1][64:68]),
            inclination=float(lines[2][8:16]),
            right_asc_node=float(lines[2][17:25]),
            eccentricity=float("0." + lines[2][26:33]),
            arg_perigee=float(lines[2][34:42]),
            mean_anomaly=float(lines[2][43:51]),
            mean_motion=float(lines[2][52:63]),
            rev_num=int(lines[2][63:68]),
        )

        print("New TLE parameters: \n")
        self.print_params()

        return

    def create_tle_from_str(self, input_str):
        """
        a TLE object is created with the string's parameters
            (assumes the string has correct formatting and \n for each of the three TLE lines)
        print_params() is called
        inputs: input_str (String)
        outputs: none
        """
        lines = input_str.split("\n")

        self.__gen_tle(
            name=lines[0].rstrip(),
            sat_num=int(lines[1][2:7]),
            classification=lines[1][7],
            int_designator=lines[1][9:17],
            epoch_year=int(lines[1][18:20]),
            epoch_day=float(lines[1][20:32]),
            mm_deriv1=float(lines[1][33] + "0" + lines[1][34:43]),
            mm_deriv2=lines[1][44:52],
            B=lines[1][53:61],
            set_num=int(lines[1][64:68]),
            inclination=float(lines[2][8:16]),
            right_asc_node=float(lines[2][17:25]),
            eccentricity=float("0." + lines[2][26:33]),
            arg_perigee=float(lines[2][34:42]),
            mean_anomaly=float(lines[2][43:51]),
            mean_motion=float(lines[2][52:63]),
            rev_num=int(lines[2][63:68]),
        )

        print("New TLE parameters: \n")
        self.print_params()

        return

    def print_params(self):
        """
        all parameters of the TLE object are printed
        inputs: none
        outputs:none
        """
        print("Name: ", self.name)
        print("Satellite number: ", self.sat_num)
        print("Classification: ", self.classification)
        print("International designator: ", self.int_designator)
        print("Epoch year: ", self.epoch_year)
        print("Epoch day: ", self.epoch_day)
        print("1st derivative of mean motion: ", self.mm_deriv1)
        print("2nd derivative of mean motion: ", self.mm_deriv2)
        print("B (drag term): ", self.B)
        print("Inclination: ", self.inclination)
        print("Right ascension of ascending node: ", self.right_asc_node)
        print("Eccentricity: ", self.eccentricity)
        print("Argument of perigee: ", self.arg_perigee)
        print("Mean anomaly: ", self.mean_anomaly)
        print("Mean motion: ", self.mean_motion)
        print("Revolution number: ", self.rev_num)
        print("Set number: ", self.set_num)

        return

    def ISS(self):
        """
        sets the tle attributes to those of the International
            Space Station (ISS) on January 1st, 2022
        inputs: none
        outputs: none
        """
        self.__gen_tle(
            name="ISS",
            sat_num=25544,
            classification="U",
            int_designator="98067A",
            epoch_year=22,
            epoch_day=1,
            mm_deriv1=-0.00002182,
            mm_deriv2=0,
            B="-11606-4",
            inclination=51.6416,
            right_asc_node=247.4627,
            eccentricity=0.0006703,
            arg_perigee=130.5360,
            mean_anomaly=325.0288,
            mean_motion=15.72125391,
            rev_num=56353,
            set_num=292,
        )
        return
