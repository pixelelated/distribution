# Seed one synthetic softcore award in the installed proxy store (the calls
# tools/ra-ui-test's guest fixture makes); the service must be stopped.
import json, time
from raofflineproxy import storage, cache_keys, config
st = storage.Storage()
st.upsert_cache(cache_keys.login('QA'), json.dumps({'User': 'QA', 'Token': 'local-ui-fixture'}))
st.upsert_cache(cache_keys.patch(100, 'QA'), json.dumps({'PatchData': {'ID': 100, 'Title': 'Local UI fixture', 'Achievements': [{'ID': 1}]}}))
st.upsert_pending_award({'achievementId': 1, 'queryString': '/dorequest.php?r=awardachievement&a=1&u=QA&h=0',
                         'requestBody': 'a=1&u=QA&h=0', 'userAgent': 'Local-UI-QA', 'queuedAt': int(time.time() * 1000)})
print('pending', len(st.get_pending_awards())); st.close()
