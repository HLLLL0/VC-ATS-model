import json

with open('data.json') as f:
    d = json.load(f)

# top roles preserved from the existing artifact for Apollo-verified companies
TOP_ROLES = {
 "679bbd962ae5f70001ce50ff": [  # Town
   {"t":"AI Product Engineer · SF · $225–300K","u":"https://jobs.ashbyhq.com/town/0b261662-60c4-49e2-b351-118e57e5714b"},
   {"t":"Staff Backend Engineer · SF · $250–300K","u":"https://jobs.ashbyhq.com/town/d54d6289-f351-4fe0-99b9-08c4467bd18b"},
   {"t":"Business Operations · SF · $130–170K","u":"https://jobs.ashbyhq.com/town/52ff57cf-4e1f-4244-8504-92a52ef0dd9c"}],
 "627961d589096b00f5a9ce56": [  # NewLimit
   {"t":"Head of Manufacturing","u":"https://job-boards.greenhouse.io/newlimit/jobs/5988743004"},
   {"t":"VP, Clinical Development","u":"https://job-boards.greenhouse.io/newlimit/jobs/5874818004"},
   {"t":"Senior Scientist, mRNA Engineering","u":"https://job-boards.greenhouse.io/newlimit/jobs/5979490004"},
   {"t":"Computational Biologist","u":"https://job-boards.greenhouse.io/newlimit/jobs/5819398004"}],
 "5ed02cefda1c7000016cc42d": [  # Supabase
   {"t":"Core Product Lead","u":"https://jobs.ashbyhq.com/supabase/f2f28afa-4b42-43c7-b977-48f5b686fba2"},
   {"t":"Product Manager – AI","u":"https://jobs.ashbyhq.com/supabase/202e9ca8-3c98-4dea-add5-0f7e2e98800c"},
   {"t":"Head of Observability","u":"https://jobs.ashbyhq.com/supabase/3d788231-c984-4bf7-bd8f-ca242988db4f"},
   {"t":"Product Security Engineer","u":"https://jobs.ashbyhq.com/supabase/8d05bc85-53f3-4ebf-b5b4-c88cdb922673"}],
 "648747c2acd90400c3a0d8d4": [  # Legora
   {"t":"Staff Software Engineer · NYC","u":"https://jobs.ashbyhq.com/legora/a7d29888-3159-4651-915a-d1a4814d1916"},
   {"t":"Engagement Manager, Enterprise · SF/NYC/Chicago","u":"https://jobs.ashbyhq.com/legora/82e9ca75-f63e-42a6-8d94-7c623c5fa922"},
   {"t":"Lead Legal Engineer · multiple cities","u":"https://jobs.ashbyhq.com/legora/c2907158-936a-441c-8f04-7c4732b83f2a"},
   {"t":"Director of Talent Acquisition · NYC","u":"https://jobs.ashbyhq.com/legora/eff6b912-3662-4c92-8417-77587b1baf49"}],
 "67e2bf15b079660011e07b94": [  # Nexthop AI
   {"t":"Manufacturing Engineer · Vietnam","u":"https://www.linkedin.com/jobs/view/4417872230/"},
   {"t":"Process Engineer · Vietnam","u":"https://www.linkedin.com/jobs/view/4417851650/"}],
 "6740a230b5a18903eb23b4bc": [  # Peec AI
   {"t":"Applied Research Scientist · Berlin","u":"https://www.linkedin.com/jobs/view/4419088872/"},
   {"t":"AI Search Manager · NYC / Berlin","u":"https://jobs.ashbyhq.com/Peec/c4f777b0-d813-4f85-b329-a211530ddf5f"},
   {"t":"Account Executive – UK&I · Berlin","u":"https://jobs.ashbyhq.com/Peec/ed4a9430-cd44-4cee-9337-f47e91678b91"}],
 "642113224f8ac100016323d4": [  # Suno
   {"t":"Senior/Staff Software Engineer, iOS · NYC","u":"https://jobs.ashbyhq.com/suno/6ae1d382-e70b-4c30-9fab-32d14d52497b"},
   {"t":"Machine Learning Scientist · Boston","u":"https://jobs.ashbyhq.com/suno/1e23d125-d72c-49b6-891d-77d62c96cd13"},
   {"t":"Sr Director, Customer Experience & Safety Ops · NYC","u":"https://jobs.ashbyhq.com/suno/3a1a46e5-7aaa-4597-b614-a5331a1e90f4"},
   {"t":"Head of Security Engineering · NYC","u":"https://jobs.ashbyhq.com/suno/5801efc0-4cef-461e-9274-30dde415a0b3"}],
 "6708da8ef227bf01b001df82": [  # Rebar
   {"t":"Software Engineer, Agentic Workflows · NYC","u":"https://jobs.ashbyhq.com/rebar/dccf8ac4-f2af-4de6-9437-a9787fa7372d"},
   {"t":"Senior ML Infrastructure Engineer · NYC","u":"https://jobs.ashbyhq.com/rebar/ead8df0c-b6da-4e79-90d0-99651cc309f5"},
   {"t":"Founding Product Manager · NYC","u":"https://jobs.ashbyhq.com/rebar/fe7f2212-aada-460e-be12-db8da8e44165"}],
}

def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')

def js_str(s):
    return '"' + esc(s) + '"'

def js_list(lst):
    return "[" + ",".join(js_str(x) for x in lst) + "]"

lines = []
lines.append("const DATA = [")
entries = []
for c in d["companies"]:
    parts = []
    if c.get("apolloId"):
        parts.append(f'apolloId:{js_str(c["apolloId"])}')
    else:
        parts.append('unverified:true')
    parts.append(f'name:{js_str(c["name"])}')
    parts.append(f'domain:{js_str(c["domain"])}')
    parts.append(f'location:{js_str(c["location"])}')
    parts.append(f'desc:{js_str(c["description"])}')
    if c.get("employees") is not None:
        parts.append(f'employees:{c["employees"]}')
    if c.get("growth6m") is not None:
        parts.append(f'growth6m:{c["growth6m"]}')
    r = c["round"]
    round_parts = [
        f'type:{js_str(r["type"])}',
        f'amountM:{r["amountM"]}',
        f'cur:{js_str(r["currency"])}',
        f'date:{js_str(r["date"])}',
        f'leads:{js_list(r["leads"])}',
        f'investors:{js_list(r["investors"])}',
        f'news:{js_str(r["newsUrl"])}',
    ]
    round_js = "{" + ",".join(round_parts) + "}"
    parts.append(f'round:{round_js}')
    j = c["jobs"]
    top = TOP_ROLES.get(c.get("apolloId"), [])
    top_js = "[" + ",".join(
        "{" + f't:{js_str(t["t"])},u:{js_str(t["u"])}' + "}" for t in top
    ) + "]"
    total_js = "null" if j.get("total") is None else str(j["total"])
    careers_val = j.get("careersUrl")
    careers_js = "null" if careers_val is None else js_str(careers_val)
    jobs_js = "{" + f'total:{total_js},careers:{careers_js},top:{top_js}' + "}"
    parts.append(f'jobs:{jobs_js}')
    entries.append("{" + ",".join(parts) + "}")

lines.append(",\n".join(entries))
lines.append("];")

with open('data_array.js', 'w') as f:
    f.write("\n".join(lines))

print("wrote data_array.js, entries:", len(entries))
