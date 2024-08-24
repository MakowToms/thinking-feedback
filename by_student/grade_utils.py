from collections import defaultdict

import pandas as pd
pd.set_option('future.no_silent_downcasting', True)

LEGEND = """Legenda:
p1 - informacje o podejściach z poziomu pierwszego (odpowiednio 2 i 3 to drugi i trzeci poziom),
ok - jedno podejście zakończone sukcesem,
B - jedno podejście z błędem,
nie - jedno podejście niepoprawne,
ZAL - umiejętność zaliczona na tym poziomie."""


convert_grade = lambda grade: "ok" if grade.value == "tick" else "nie" if grade.value == "cross" else grade.value


def get_passed_levels(levels, min_passes=2):
    passed_levels = []
    for level, g in levels.items():
        convert = lambda val: "✔" if val == "tick" else "✘" if val == "cross" else val
        g_str = ''.join([convert(grade.value) for grade in g])
        streaks = g_str.split("✘")
        passed = False
        for streak in streaks:
            if streak.__contains__("✔"):
                oks = streak.count("✔")
                bs = streak.count("B")
                if bs + oks*2 >= min_passes * 2:
                    passed = True
                # if len(streak) == min_passes and streak[0] == "✔" and streak[1] == "✔":
                #     passed = True
                # if len(streak) >= 3 and streak.__contains__("✔"):
                #     passed = True
        if passed:
            passed_levels.append(int(level))
    return passed_levels


VALUE_TO_INT = {
    "tick": 2,
    "B": 1,
    "cross": 0,
}
INT_TO_VALUE = {
    2: "✔",
    1: "B",
    0: "✘",
}
INT_TO_LIBRUS = {
    2: "ok",
    1: "B",
    0: "nie",
}


def convert_grades_to_table(grades):
    grades_dict = defaultdict(lambda: defaultdict(list))
    for grade in grades:
        grades_dict[int(grade.skill_level.level)][grade.publish_date.date()] = VALUE_TO_INT[grade.value]
    pd_grades = pd.DataFrame(grades_dict, columns=[1, 2, 3])
    pd_grades = pd_grades.fillna(-1)
    pd_grades = pd_grades.convert_dtypes()
    pd_grades = pd_grades.sort_index()
    # print(pd_grades)
    for index, row in pd_grades.iterrows():
        if row[3] > row[2] and row[3] >= 1:
            row[2] = row[3]
        if row[2] > row[1] and row[2] >= 1:
            row[1] = row[2]
        pd_grades.loc[index, :] = row
    passed_levels = []
    for index, column in pd_grades.items():
        cur_val = 0
        was_done = False
        for val in column:
            if val == 0:
                cur_val = 0
                was_done = False
            if val > 0:
                cur_val += val
            if val == 2:
                was_done = True
            if cur_val >= 4 and was_done:
                passed_levels.append(index)
    passed_level = max(passed_levels) if len(passed_levels) > 0 else 0
    table = ""
    level_grades = {}
    for index, column in pd_grades.items():
        if index <= passed_level:
            table += f"(p{index}: ZAL);"
            level_grades[index] = ["ZAL"]
        else:
            level_grades[index] = [INT_TO_VALUE[val] for val in column if val!=-1]
            table += f"(p{index}: {','.join([INT_TO_LIBRUS[val] for val in column if val!=-1])});"
    return table, level_grades
