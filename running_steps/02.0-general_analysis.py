## 2 General Stat

import pandas as pd
from pathlib import Path

from src.analysistools import (get_yearly_paper_counts,
                               display_paper_yearly,
                               calc_yearly_avg_authors,
                               display_authorship_yearly)


intput_file_path = Path("../data/02-processed-data")
intput_file_name = intput_file_path/"epb_cleaned_abs.csv"
#load data
paper_df = pd.read_csv(intput_file_name)

if __name__ == "__main__":
    ### 1 Yearly Publication Statistics: Count total papers published per year
    paper_year_df = get_yearly_paper_counts(paper_df)
    display_paper_yearly(
        data=paper_year_df,
        year_gap=4,
        output_dir="../data/04-resulting-data"
    )

    ### 2 Co-author Statistics: Calculate average number of authors per paper by year
    avg_authors_df = calc_yearly_avg_authors(paper_df)
    display_authorship_yearly(
        data=avg_authors_df,
        year_gap=4,
        output_dir="../data/04-resulting-data"
    )
