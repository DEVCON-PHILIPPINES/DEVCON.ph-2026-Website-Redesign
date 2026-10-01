# Nested URL structure for the deployed site: file stem -> folder path (no leading/trailing slash; '' = home)
CITIES = ['manila','laguna','legazpi','pampanga','cebu','iloilo','bohol','bacolod','tacloban','davao','cagayandeoro','iligan','bukidnon']
PATHS = {'index': '',
  'about': 'about', '17years': 'about/17years', 'leadership': 'about/leadership',
  'programs': 'programs', 'devcon-kids': 'programs/kids', 'campus': 'programs/campus', 'sheisdevcon': 'programs/sheisdevcon',
  'pro-summit': 'programs/pro-summit', 'crest': 'programs/crest', 'dctx': 'programs/dctx', 'educators': 'programs/educators',
  'ai-fluency-masterclass': 'programs/ai-fluency-agentic-training', 'ai-code-camps': 'programs/ai-code-camps',
  'jumpstart-internships': 'programs/jumpstart-internships', 'ai': 'programs/ai-scholarships',
  'chapters': 'locations',
  'devrel-case-studies': 'case-studies',
  'case-study-sui': 'case-studies/sui', 'case-study-icp': 'case-studies/icp', 'case-study-hour-of-ai': 'case-studies/hour-of-ai',
  'case-study-zoho-creator': 'case-studies/zoho-creator', 'case-study-campus-devcon-summit': 'case-studies/campus-devcon-summit',
  'case-study-pro-summit': 'case-studies/pro-summit', 'case-study-mindanao-ai-caravan': 'case-studies/mindanao-ai-caravan',
  'case-study-ai-physical-computing-educators': 'case-studies/ai-physical-computing-educators',
  'case-study-devcon-for-educators': 'case-studies/devcon-for-educators', 'case-study-microbit': 'case-studies/microbit',
  'playbook': 'playbook', 'brand-kit': 'playbook/brand-kit', 'volunteers-guide': 'playbook/volunteers-guide',
  'code-of-conduct-for-national-and-chapter-officers-and-volunteers': 'playbook/code-of-conduct',
  'standard-privacy-and-safespace-consent': 'playbook/privacy-and-safe-space', 'child-protection-policy': 'playbook/child-protection-policy',
  'campus-events-guidelines': 'playbook/campus-events-guidelines',
  'attend': 'attend', 'invite': 'invite', 'partner': 'partner'}
for _c in CITIES: PATHS[_c] = f'locations/{_c}'
def path_of(stem): return PATHS.get(stem, stem)
