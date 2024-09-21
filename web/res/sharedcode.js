let mouseX = 0;
let mouseY = 0;

document.addEventListener("mousemove", (event) => {
    mouseX = event.clientX;
    mouseY = event.clientY;
});

function popup(title) {
    const root = document.createElement("div");
    root.id = "popuproot";

    root.style.width = "330px";
    root.style.height = "230px";
    root.style.backgroundColor = "#8d99ae";
    root.style.left = "50%";
    root.style.top = "50%";
    root.style.position = "absolute";
    root.style.transform = "translate(-50%, -50%)";
    root.style.borderRadius = "5px";

    root.innerHTML = `
    <h3 style="font-family: system-ui; color: white; margin: 0; padding: 5px; width: 320px; max-width: 320px; min-width: 320px; background-color: #ef233c; border-radius: 5px;">${title}</h3>
    `;

    const content = document.createElement("div");
    content.id = "popupcontent";

    content.style.display = "flex";
    content.style.flexDirection = "column";

    disableAll();

    document.body.appendChild(root);
    root.appendChild(content);

    return [root, content];
}

function enableAll() {
    const buttons = document.querySelectorAll("button");
    buttons.forEach((button) => (button.disabled = false));

    const links = document.querySelectorAll("a");
    links.forEach((link) => (link.style.pointerEvents = "auto"));
}

function disableAll() {
    const buttons = document.querySelectorAll("button");
    buttons.forEach((button) => {
        if (!button.closest("#nav-items")) {
            button.disabled = true;
        }
    });

    const links = document.querySelectorAll("a");
    links.forEach((link) => {
        if (!link.closest("#nav-items")) {
            link.style.pointerEvents = "none";
        }
    });
}

let currentMenu = null;

function contextmenu() {
    document.querySelectorAll('#contextmenu').forEach(element => element.remove());

    const root = document.createElement("div");
    root.style.position = "absolute";
    root.style.left = `${mouseX}px`;
    root.style.top = `${mouseY}px`;
    root.style.backgroundColor = "#8d99ae";
    root.style.padding = "15px";
    root.style.borderRadius = "5px";
    root.style.display = "flex";
    root.style.flexDirection = "column";
    root.style.opacity = "0";
    root.style.transition = "all 0.2s ease-in-out";
    root.style.fontFamily = "system-ui";
    root.style.color = "#202231";
    root.style.gap = '5px'
    root.id = 'contextmenu'
    document.body.appendChild(root);

    setTimeout(() => {
        requestAnimationFrame(() => {
            root.style.opacity = "1";
        });
    }, 1);

    currentMenu = root;

    return root;
}

function hideMenu(event) {
    document.querySelectorAll('#contextmenu').forEach(element => element.remove());
    currentMenu = null;
}

document.addEventListener("click", hideMenu);
