# %%
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('sqlite://', echo=False)


# %%
keywords = pd.read_csv("data/output/keywords.csv", index_col=0)
keywords["keyword_id"] = keywords["keyword_id"].astype(int)
keywords.head()


# %%
df = pd.DataFrame({'name' : ['User 1', 'User 2', 'User 3']})
df

# %%
df.to_sql('users', con=engine)

# %%
engine.execute("SELECT * FROM users").fetchall()

# %%
