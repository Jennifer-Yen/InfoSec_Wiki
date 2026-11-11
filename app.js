const search = document.querySelector("#search");
const groups = [...document.querySelectorAll(".group")];
const results = document.querySelector("#results");

function filterNotes() {
  const terms = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
  let total = 0;
  for (const group of groups) {
    let matches = 0;
    for (const note of group.querySelectorAll("[data-note]")) {
      const text = note.dataset.search.toLowerCase();
      note.hidden = !terms.every(term => text.includes(term));
      if (!note.hidden) matches++;
    }
    group.hidden = matches === 0;
    total += matches;
  }
  results.textContent = total ? total + " 篇筆記" : "找不到符合的筆記";
}

search.addEventListener("input", filterNotes);
filterNotes();
