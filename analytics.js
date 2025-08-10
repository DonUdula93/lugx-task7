function sendEvent(eventType, additionalData = {}) {
    const payload = {
        session_id: sessionStorage.getItem("session_id") || (function () {
            const id = crypto.randomUUID();
            sessionStorage.setItem("session_id", id);
            return id;
        })(),
        event_type: eventType,
        page_url: window.location.href,
        timestamp: new Date().toISOString(),
        ...additionalData
    };

    fetch("/track", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    }).then(response => {
        if (!response.ok) {
            console.error("Failed to send analytics event:", response.statusText);
        }
    }).catch(error => {
        console.error("Error sending event:", error);
    });
}

window.addEventListener("DOMContentLoaded", () => {
    sendEvent("page_view");

    let startTime = Date.now();

    window.addEventListener("beforeunload", () => {
        const timeSpent = (Date.now() - startTime) / 1000;
        sendEvent("page_exit", { time_on_page: timeSpent });
    });

    window.addEventListener("scroll", () => {
        const scrollDepth = Math.floor(window.scrollY / (document.body.scrollHeight - window.innerHeight) * 100);
        sendEvent("scroll", { scroll_depth: scrollDepth });
    });

    document.body.addEventListener("click", (e) => {
        if (e.target.id) {
            sendEvent("click", { element_id: e.target.id });
        }
    });
});

