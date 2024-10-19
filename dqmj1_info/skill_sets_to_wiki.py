from typing import List, Set, Tuple

import argparse
import ast
import pathlib
import string
import sys

import pandas as pd

TEMPLATE = """{{Stub}}
'''$name''' is the $id_with_suffix [[Skillsets|skill]] of the library in {{dqmj}}.

{{Skillset
|title   = $name
|number  = $id
|caption = $description
|skill1  = $skill_1
|point1  = $points_1
|skill2  = $skill_2
|point2  = $points_2
|skill3  = $skill_3
|point3  = $points_3
|skill4  = $skill_4
|point4  = $points_4
|skill5  = $skill_5
|point5  = $points_5
|skill6  = $skill_6
|point6  = $points_6
|skill7  = $skill_7
|point7  = $points_7
|skill8  = $skill_8
|point8  = $points_8
|skill9  = $skill_9
|point9  = $points_9
|skill10 = $skill_10
|point10 = $points_10
|first_skillset  = $first_skillset
|second_skillset = $second_skillset
|third_skillset  = $third_skillset
}}

==Monsters with $name==
{{Monster list|Monsters with $name_escaped}}

==Rival Monsters with $name==
{{Monster list|Rival monsters with $name_escaped}}
"""


def main(argv: List[str]) -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("--skill_sets_csv", required=True)
    parser.add_argument("--string_tables_csv", required=True)
    parser.add_argument("--output_directory", type=pathlib.Path, required=True)

    args = parser.parse_args(argv)

    skill_sets = pd.read_csv(args.skill_sets_csv)
    string_tables = pd.read_csv(args.string_tables_csv)
    output_directory = args.output_directory

    assert isinstance(output_directory, pathlib.Path)

    output_directory.mkdir(exist_ok=True, parents=True)

    monster_names = {
        str(name).lower()
        for name in string_tables[
            string_tables["table_name"] == "monster_species_names"
        ]["string"]
    }
    skill_sets["can_upgrade"] = skill_sets["can_upgrade"] == "Yes"
    skill_sets["name"] = [str(name) for name in skill_sets["name"]]

    columns_to_parse = ["skill_point_requirements", "skill_names", "trait_names"]
    for column in columns_to_parse:
        skill_sets[column] = skill_sets[column].apply(lambda x: ast.literal_eval(x))

    template = string.Template(TEMPLATE)

    for i, row in skill_sets.iterrows():
        print(f'{i:03d} - {row["name"]}')
        skills_and_traits = []
        for j in range(0, 10):
            skill_names = row["skill_names"][j]
            skill_name = skill_names[0] if len(skill_names) > 0 else None

            trait_names = row["trait_names"][j]
            trait_name = trait_names[0] if len(trait_names) > 0 else None

            skills_and_traits.append(
                (
                    row["skill_point_requirements"][j],
                    " / ".join([n for n in [skill_name, trait_name] if n is not None]),
                )
            )

            if row["skill_point_requirements"][j] == row["max_skill_points"]:
                break

        assert isinstance(i, int)

        skillset_line = get_skillset_line(skill_sets, i)

        filepath = output_directory / f'{i:03d} - {row["name"]}.txt'
        with open(filepath, "w", encoding="utf8") as output_stream:
            output_stream.write(
                clean_page(
                    template.substitute(
                        name=sanitize_name(row["name"]),
                        name_escaped=deregex(
                            sanitize_name(deconflict_name(row["name"], monster_names))
                        )
                        + "$",
                        id=i,
                        id_with_suffix=add_number_suffix(i),
                        description=row["description"],
                        points_1=get_skill_or_trait(skills_and_traits, 0, 0),
                        skill_1=get_skill_or_trait(skills_and_traits, 0, 1),
                        points_2=get_skill_or_trait(skills_and_traits, 1, 0),
                        skill_2=get_skill_or_trait(skills_and_traits, 1, 1),
                        points_3=get_skill_or_trait(skills_and_traits, 2, 0),
                        skill_3=get_skill_or_trait(skills_and_traits, 2, 1),
                        points_4=get_skill_or_trait(skills_and_traits, 3, 0),
                        skill_4=get_skill_or_trait(skills_and_traits, 3, 1),
                        points_5=get_skill_or_trait(skills_and_traits, 4, 0),
                        skill_5=get_skill_or_trait(skills_and_traits, 4, 1),
                        points_6=get_skill_or_trait(skills_and_traits, 5, 0),
                        skill_6=get_skill_or_trait(skills_and_traits, 5, 1),
                        points_7=get_skill_or_trait(skills_and_traits, 6, 0),
                        skill_7=get_skill_or_trait(skills_and_traits, 6, 1),
                        points_8=get_skill_or_trait(skills_and_traits, 7, 0),
                        skill_8=get_skill_or_trait(skills_and_traits, 7, 1),
                        points_9=get_skill_or_trait(skills_and_traits, 8, 0),
                        skill_9=get_skill_or_trait(skills_and_traits, 8, 1),
                        points_10=get_skill_or_trait(skills_and_traits, 9, 0),
                        skill_10=get_skill_or_trait(skills_and_traits, 9, 1),
                        first_skillset=sanitize_name(
                            deconflict_name(skillset_line[0], monster_names)
                        ),
                        second_skillset=sanitize_name(
                            deconflict_name(skillset_line[1], monster_names)
                        ),
                        third_skillset=sanitize_name(
                            deconflict_name(skillset_line[2], monster_names)
                        ),
                    )
                )
            )


def deconflict_name(name: str, deconflict_names: Set[str]) -> str:
    if name.lower() in deconflict_names:
        return f"{name} (skill)"

    return name


def sanitize_name(name: str) -> str:
    return str(name).replace("Ⅱ", "II").replace("Ⅲ", "III")


def deregex(name: str) -> str:
    return name.replace("(", "\\(").replace(")", "\\)")


def get_skillset_line(skill_sets: pd.DataFrame, i: int) -> Tuple[str, str, str]:
    skillset_line = []

    current = i
    while True:
        if current >= len(skill_sets):
            break

        skillset_line.append(current)

        if not skill_sets["can_upgrade"][current]:
            break

        current += 1

    current = i - 1
    while True:
        if current < 0:
            break

        if not skill_sets["can_upgrade"][current]:
            break

        skillset_line.insert(0, current)
        current -= 1

    assert 1 <= len(skillset_line) <= 3

    if len(skillset_line) == 1:
        return ("", "", "")
    elif len(skillset_line) == 3:
        return (
            skill_sets["name"][skillset_line[0]],
            skill_sets["name"][skillset_line[1]],
            skill_sets["name"][skillset_line[2]],
        )
    else:
        assert len(skillset_line) == 2

        if skill_sets["max_skill_points"][skillset_line[0]] == 50:
            return (
                skill_sets["name"][skillset_line[0]],
                skill_sets["name"][skillset_line[1]],
                "",
            )
        else:
            return (
                "",
                skill_sets["name"][skillset_line[0]],
                skill_sets["name"][skillset_line[1]],
            )


def clean_page(page: str) -> str:
    lines = []
    for line in page.split("\n"):
        if line.endswith(" = "):
            continue

        lines.append(line)

    return "\n".join(lines)


def get_skill_or_trait(data: List[Tuple[str, str]], i: int, j: int) -> str:
    try:
        return data[i][j]
    except IndexError:
        return ""


def add_number_suffix(num: int) -> str:
    suffix = None

    last_digit = num % 10
    two_last_digits = num % 100

    if last_digit == 1 and two_last_digits != 11:
        suffix = "st"
    elif last_digit == 2 and two_last_digits != 12:
        suffix = "nd"
    elif last_digit == 3 and two_last_digits != 13:
        suffix = "rd"
    else:
        suffix = "th"

    assert suffix is not None

    return f"{num}{suffix}"


if __name__ == "__main__":
    main(sys.argv[1:])
