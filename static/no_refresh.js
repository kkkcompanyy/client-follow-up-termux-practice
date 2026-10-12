/*
  Educational practice copy.
  This is NOT the user's private production no_refresh.js.

  It intercepts Quick Action submissions, sends the same POST with
  X-Requested-With: XMLHttpRequest, and updates the visible row.
*/
document.addEventListener("submit", async function (event) {
    const button = event.submitter;

    if (!button || !button.classList.contains("quick-button")) {
        return;
    }

    if (button.dataset.normalSubmit === "1") {
        delete button.dataset.normalSubmit;
        return;
    }

    event.preventDefault();

    const form = button.form;
    const action = button.getAttribute("formaction") || form.action;
    const method = button.getAttribute("formmethod") || form.method || "POST";
    const row = button.closest("tr");

    button.disabled = true;

    try {
        const response = await fetch(action, {
            method: method.toUpperCase(),
            body: new FormData(form),
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        });

        if (!response.ok) {
            throw new Error("Server returned " + response.status);
        }

        if (!row) {
            return;
        }

        const status = row.querySelector(".status");
        const calledAt = row.querySelector(".called-at-cell");

        if (!status) {
            return;
        }

        const wasCalled =
            status.classList.contains("yes") ||
            status.textContent.trim().toUpperCase() === "CALLED";

        const isCalled = !wasCalled;

        status.classList.toggle("yes", isCalled);
        status.classList.toggle("no", !isCalled);
        status.textContent = isCalled ? "CALLED" : "NOT CALLED";
        button.textContent = isCalled ? "Mark NO" : "Mark YES";

        if (calledAt) {
            if (isCalled) {
                const now = new Date();
                const dd = String(now.getDate()).padStart(2, "0");
                const mm = String(now.getMonth() + 1).padStart(2, "0");
                const yyyy = now.getFullYear();
                const hh = String(now.getHours()).padStart(2, "0");
                const min = String(now.getMinutes()).padStart(2, "0");

                calledAt.textContent =
                    `${dd}/${mm}/${yyyy} · ${hh}:${min}`;
            } else {
                calledAt.textContent = "—";
            }
        }

        const calledNumber =
            document.querySelector(".called-card .stat-number");
        const pendingNumber =
            document.querySelector(".pending-card .stat-number");

        if (calledNumber && pendingNumber) {
            let called = parseInt(calledNumber.textContent, 10) || 0;
            let pending = parseInt(pendingNumber.textContent, 10) || 0;

            if (isCalled) {
                called += 1;
                pending = Math.max(0, pending - 1);
            } else {
                called = Math.max(0, called - 1);
                pending += 1;
            }

            calledNumber.textContent = String(called);
            pendingNumber.textContent = String(pending);
        }
    } catch (error) {
        console.error("Quick Action AJAX failed; using normal form submit.", error);

        // Safe fallback: let Flask handle the normal POST/redirect.
        button.dataset.normalSubmit = "1";
        form.requestSubmit(button);
    } finally {
        button.disabled = false;
    }
});
