document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        // build participants list markup
        // build participants list markup (with remove icons)
        const participantList = details.participants.length
          ? `<ul class="participant-list">${details.participants
              .map(
                (p) =>
                  `<li class="participant-item"><span class="email">${p}</span><button class="remove" data-activity="${name}" data-email="${p}">&times;</button></li>`
              )
              .join('')}</ul>`
          : '<p class="no-participants"><em>No one has signed up yet.</em></p>';

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          <div class="participants">
            <strong>Participants:</strong>
            ${participantList}
          </div>
        `;

        // attach remove handlers for any delete buttons just added
        activityCard.querySelectorAll('.remove').forEach((btn) => {
          btn.addEventListener('click', async (e) => {
            const activityName = e.target.dataset.activity;
            const emailToRemove = e.target.dataset.email;
            try {
              const resp = await fetch(
                `/activities/${encodeURIComponent(activityName)}/signup?email=${encodeURIComponent(emailToRemove)}`,
                { method: 'DELETE' }
              );
              if (resp.ok) {
                // refresh list to reflect removal
                fetchActivities();
              } else {
                const err = await resp.json();
                console.error('Failed to remove participant', err);
              }
            } catch (err) {
              console.error('Error removing participant', err);
            }
          });
        });

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        // refresh activities to show new participant and updated spot count
        fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
