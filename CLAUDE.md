# Claude Instructions

## Last Known Good Commit
2f7f6defe84121b731e8193fe190e27c45f42416 - Before RSS/Atom implementation

## Styling Policy
- NEVER add CSS styles unless explicitly requested
- Keep styling extremely minimal - web 1.0 style intentionally
- Only modify existing styles when directly asked
- Default browser styling is preferred over custom styling

## Golden/Blue Hour Feature Ideas
**Zero build tools needed:**
```html
<script src="https://cdn.jsdelivr.net/npm/suncalc@1.9.0/suncalc.min.js"></script>
<script>
// Your code here - SunCalc is now available globally
</script>
```

**Or even simpler - just copy the library:**
SunCalc.js is only ~100 lines of code. You could literally copy it into your `static/` folder and include it like any other JS file.

**Minimal implementation:**
```html
<div id="sun-times"></div>
<script src="https://cdn.jsdelivr.net/npm/suncalc@1.9.0/suncalc.min.js"></script>
<script>
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(pos => {
    const times = SunCalc.getTimes(new Date(), pos.coords.latitude, pos.coords.longitude);
    document.getElementById('sun-times').innerHTML = 
      `Golden hour: ${times.goldenHour.toLocaleTimeString()} - ${times.goldenHourEnd.toLocaleTimeString()}`;
  });
}
</script>
```