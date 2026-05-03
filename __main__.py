from utils import input_utils
from pathlib import Path
import runpy



def main():
    file_path: Path = Path(__file__).parent.resolve()
    chapters: list[str] =  ["Chapter " + f.name.removeprefix("Chapter") for f in file_path.iterdir() if f.is_dir() and "Chapter" in f.name]

    chapters_to_do = input_utils.select_from_list(chapters, prompt="Enter Chapters to review.", select_multiple=True)

    for chapter in chapters_to_do:
        print(f"Executing {chapter}")
        chapter_path = chapter.replace(" ", "")
        runpy.run_module(chapter_path, run_name="__main__")





if __name__ == "__main__":
    main()