const filterButtons = document.querySelectorAll(".filter-btn");
const cards = document.querySelectorAll(".demo-card");
const emptyState = document.querySelector(".empty-state");

const applyFilter = (category) => {
  let visible = 0;

  cards.forEach((card) => {
    const match = category === "all" || card.dataset.category === category;
    card.classList.toggle("hidden", !match);
    if (match) visible += 1;
  });

  if (emptyState) {
    emptyState.classList.toggle("visible", visible === 0);
  }
};

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    filterButtons.forEach((btn) => {
      btn.classList.remove("active");
      btn.setAttribute("aria-pressed", "false");
    });
    button.classList.add("active");
    button.setAttribute("aria-pressed", "true");
    applyFilter(button.dataset.filter);
  });
});

applyFilter("all");
