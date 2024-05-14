import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

graph_dir = 'graphs/'
if not os.path.exists(graph_dir):
    exit

df = pd.read_csv('cissm_databse_export_csv_here')
top_actors = df[df['actor'] != 'Undetermined']['actor'].value_counts().head(7).index.tolist() # t7
df_top_actors = df[df['actor'].isin(top_actors)]

df['event_date'] = pd.to_datetime(df['event_date'])
df_filtered = df[(df['event_date'].dt.year >= 2014) & (df['actor_type'] != 'Undetermined')]
actor_type_count = df_filtered.groupby([pd.Grouper(key='event_date', freq='M'), 'actor_type']).size().unstack()

df_removed_und = df[df['motive'] != 'Undetermined']
motive_count_removed_und = df_removed_und.groupby(['event_type', 'motive']).size().unstack()


sns.countplot(data=df_top_actors, x='actor', order=df_top_actors['actor'].value_counts().index)
plt.title('Count of Events by Top 7 Actors (Excluding "Undetermined")')
plt.xlabel('Actor')
plt.ylabel('Count')
plt.xticks(rotation=45)
# plt.savefig(os.path.join(graph_dir, 'count_of_events_by_top_actors.png'))
plt.show()

df['actor_type'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Actor Type Distribution')
plt.ylabel('')
# plt.savefig(os.path.join(graph_dir, 'actor_type_distribution.png'))
plt.show()

sns.boxplot(data=df_filtered, x=df_filtered['event_date'].dt.year, y='actor_type')
plt.title('Box Plot Timeline of Cyber Attacks (2010 to Current Year)')
plt.xlabel('Year')
plt.ylabel('Count')
plt.xticks(rotation=45)
# plt.savefig(os.path.join(graph_dir, 'box_plot_timeline.png'))
plt.show()

df['event_type'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Event Type Distribution')
plt.ylabel('')
# plt.savefig(os.path.join(graph_dir, 'event_type_distribution.png'))
plt.show()

sns.lineplot(data=actor_type_count, markers=True)
plt.title('Count of Events by Actor Type Over Time (From 2014, Excluding "Undetermined")')
plt.xlabel('Date')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend(title='Actor Type', loc='upper left', fontsize='large')
plt.tight_layout()
# plt.savefig(os.path.join(graph_dir, 'count_of_events_by_actor_type_over_time.png'))
plt.show()

ax = motive_count_removed_und.plot(kind='bar', stacked=True)
plt.title('Event Type by Motive')
plt.xlabel('Event Type')
plt.ylabel('Count')
plt.xticks(rotation=45)
for p in ax.patches: # number and padding problem
    width = p.get_width()
    height = p.get_height()
    x, y = p.get_xy()
    ax.annotate(f'{height}', (x + width / 2, y + height / 2), ha='center', va='center')
plt.legend(title='Motive', loc='upper right', fontsize='medium')
plt.tight_layout()
# plt.savefig(os.path.join(graph_dir, 'event_type_by_motive.png'))
plt.show()