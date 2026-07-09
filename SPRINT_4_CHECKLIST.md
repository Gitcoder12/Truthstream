# Sprint 4: Run & Stabilize — Complete Checklist

**Status:** ✅ READY FOR LOCAL TESTING

## 🚀 Quick Start

```bash
# Terminal 1: Backend
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
uvicorn truthstream.api:app --reload

# Terminal 2: Frontend
cd frontend
npm install
npm run dev

# Open http://127.0.0.1:5173
```

---

## ✅ Verification Checklist

After both servers are running, verify each feature:

### Core Functionality
- [ ] Website opens at http://127.0.0.1:5173
- [ ] Backend health check: `curl http://127.0.0.1:8000/health` returns `{"status": "ok"}`
- [ ] No CORS errors in browser console (F12)
- [ ] No TypeScript errors during `npm run build`
- [ ] All tests pass: `pytest`

### UI & Navigation
- [ ] Home page displays with tagline and buttons
- [ ] Navigation bar shows: Home, Verify, History, About, Settings
- [ ] TruthStream logo and title visible
- [ ] Navigation buttons are clickable
- [ ] No layout issues or missing content

### Verify Page
- [ ] Input field accepts text
- [ ] "Verify claim" button is clickable
- [ ] Loading spinner shows while verifying
- [ ] Try: `"India banned AI systems"`
- [ ] Result appears with:
  - Confidence score (0-100%)
  - Status (Likely True/False/Mixed/Insufficient)
  - Claim text
  - Evidence cards

### Confidence Meter
- [ ] Displays large percentage (e.g., "0%")
- [ ] Gradient bar fills from left based on confidence
- [ ] Status badge shows appropriate label
- [ ] Colors: Red (low) → Amber (medium) → Green (high)
- [ ] Responsive on mobile

### Evidence Display
- [ ] Supporting evidence shows in green cards (if any)
- [ ] Contradicting evidence shows in red cards
- [ ] Neutral evidence shows in blue cards
- [ ] Each card shows:
  - Title
  - Snippet (text preview)
  - Source name
  - Credibility percentage
  - "Open source" link (where applicable)
- [ ] Cards are readable and not cut off

### Source Links
- [ ] "Open source ↗" link is clickable
- [ ] Opens in new tab (target="_blank")
- [ ] Links are not broken (valid URLs)

### History Page
- [ ] Verify a claim first (enables history)
- [ ] Navigate to History page
- [ ] Previous verification appears with:
  - Timestamp
  - Original claim
  - Full result panel
- [ ] Multiple verifications show in reverse chronological order
- [ ] "Clear history" button is visible and clickable
- [ ] Clearing history removes all items
- [ ] Empty state shows when no history

### Settings Page
- [ ] API base URL field shows `/api`
- [ ] Can edit URL
- [ ] Dark mode toggle switches theme
- [ ] Save history toggle controls history storage
- [ ] Settings persist when page reloads
- [ ] All toggles respond visually

### Dark Mode
- [ ] Default theme is dark (dark background, light text)
- [ ] Toggle in Settings switches to light mode
- [ ] All pages respect the theme:
  - Text color changes
  - Background color changes
  - Card backgrounds change
  - Smooth transitions (no jarring flashes)
- [ ] Theme persists when page reloads

### About Page
- [ ] Shows 4-step verification flow
- [ ] Each step shows:
  - Number badge
  - Title
  - Description
- [ ] Content is readable and properly formatted

### Responsive Design
- [ ] Mobile (< 640px):
  - Navigation stacks vertically
  - Single column layout
  - Cards stack properly
  - Buttons are tap-friendly (> 44px)
- [ ] Tablet (640-1024px):
  - 2-column layout where applicable
  - Navigation horizontal
  - Evidence cards in grid
- [ ] Desktop (> 1024px):
  - Full width layout
  - Navigation with spacing
  - Evidence cards in multi-column grid
  - All content readable

### API Integration
- [ ] Verify page sends POST to `/api/verify`
- [ ] Backend responds with results
- [ ] Results render correctly
- [ ] Error handling works (try empty text)
- [ ] Settings API URL change affects requests

### Error Handling
- [ ] Empty claim shows error: "Enter a claim before verifying."
- [ ] Network error shows: "Verification failed with status..."
- [ ] Invalid API URL shows appropriate error
- [ ] Errors don't crash the app

### Performance
- [ ] Verification completes within 2 seconds (demo mode)
- [ ] Page loads without lag
- [ ] Typing in input field is responsive
- [ ] Theme toggle is smooth
- [ ] No console warnings or errors

---

## 📋 Backend Tests

```bash
pytest -v
```

Expected output:
```
test_health_endpoint PASSED
test_verify_endpoint PASSED
test_verify_endpoint_rejects_empty_text PASSED
test_verify_batch_endpoint_preserves_order PASSED
test_pipeline_contradicts_unsupported_ai_ban_claim PASSED
test_pipeline_reports_insufficient_evidence_for_unknown_claim PASSED
test_wikipedia_provider_maps_search_results_to_neutral_evidence PASSED
test_crossref_provider_maps_work_metadata PASSED
test_openalex_provider_maps_work_metadata PASSED
test_cached_provider_reuses_claim_response PASSED
test_composite_retriever_keeps_working_when_provider_fails PASSED

✅ 11 passed
```

---

## 🔧 Troubleshooting

### Frontend won't start
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Backend dependency error
```bash
pip install --upgrade pip
pip install -e '.[dev]'
pytest  # Check for import errors
```

### Port 5173 already in use
```bash
cd frontend
npm run dev -- --port 5174
# Then update Settings page API URL if needed
```

### Port 8000 already in use
```bash
uvicorn truthstream.api:app --reload --port 8001
# Then update Settings page API URL to http://127.0.0.1:8001
```

### TypeScript errors
```bash
cd frontend
npm run build  # Shows all errors
```

### CORS errors
- Verify backend is running
- Check Settings page API URL
- Vite proxy should handle `/api` → `http://127.0.0.1:8000`
- If direct URL, enable CORS on FastAPI

---

## 📊 Test Examples

### Claim 1: AI Ban (Contradicted)
```
Input: "India banned AI systems."
Expected Status: likely_false
Expected Confidence: 0%
Expected Evidence: 2 contradicting
```

### Claim 2: Unknown (Insufficient Evidence)
```
Input: "The moon has a new public library."
Expected Status: insufficient_evidence
Expected Confidence: 50%
Expected Evidence: 0 supporting, 0 contradicting
```

### Claim 3: Misinformation (Supported)
```
Input: "Recent research on multilingual misinformation is rising."
Expected Status: likely_true
Expected Confidence: > 50%
Expected Evidence: Supporting evidence
```

---

## 🎯 Definition of Done

✅ All 11 verification checklist items pass
✅ All 11 backend tests pass
✅ Zero console errors or warnings
✅ All responsive breakpoints verified
✅ Settings/history/dark mode persist correctly
✅ API integration works seamlessly
✅ Error handling graceful
✅ Documentation updated

**Result:** Fully functional, production-ready MVP ready for deployment.

---

## 📝 Next Steps

1. ✅ **This Sprint:** Verify all checklist items locally
2. 🎯 **Next Sprint:** Deploy to staging environment
3. 🚀 **Production:** Public API + analytics
4. 📈 **Scale:** Add persistent database, user auth, more providers

---

## ✨ Completion

Once all checklist items pass:

1. Create pull request to merge `sprint-4-run-stabilize` → `main`
2. Document any findings in PR description
3. Tag version as `0.1.0-rc1` (Release Candidate 1)
4. Ship! 🚀
