const socket = io("http://localhost:80");

socket.on("connect", () => {
    console.log("Received connect message, connection established!");
});

let previousServers = [];

async function getServers() {
    try {
        const response = await fetch("/api/getservers");
        if (!response.ok) {
            throw new Error(
                `Network response was not ok: ${response.statusText}`
            );
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching servers:", error);
        return []; // Return an empty array to avoid errors in the loop
    }
}

function serversAreEqual(servers1, servers2) {
    if (servers1.length !== servers2.length) {
        return false;
    }
    for (let i = 0; i < servers1.length; i++) {
        if (
            servers1[i].id !== servers2[i].id ||
            servers1[i].name !== servers2[i].name
        ) {
            return false;
        }
    }
    return true;
}

async function updateServers() {
    const servers = await getServers();

    if (serversAreEqual(previousServers, servers)) {
        return;
    }

    currentServers = servers

    const element = document.getElementById("servercontent");

    let html = ``;

    servers.forEach((server) => {
        html += `<a id="server" server="${server[0]}">
                    <label server="${server[0]}" id="servericon" class="material-symbols-rounded">dns</label>
                    <label server="${server[0]}" id="serverid">#${server[0]}</label>
                    <label server="${server[0]}" id="servername">${server[1]}</label>
                </a>`;
    });

    element.innerHTML = html;
    previousServers = servers;
}

function addserverprompt() {
    const popupContent = `
    <label style=\"font-family: system-ui; color: white; margin-top: 10px; margin-left: 10px;\">
      Name
    </label>
    <input type=\"text\" id=\"servercreatename\" style=\"width: 50%; margin: 10px;\">
    
    <label style=\"font-family: system-ui; color: white; margin-top: 10px; margin-left: 10px;\">
      Port
    </label>
    <input type=\"number\" id=\"servercreateport\" style=\"width: 50%; margin: 10px;\">
    
    <div style=\"display: flex; justify-content: center; margin-top: 25px; gap: 5px;\">
      <button style=\"background: #BDE363; border: none; border-radius: 5px; padding: 5px; cursor: pointer; color: white;\" id=\"doneButton\" onclick=\"createServer();\">
        Done
      </button>
      <button style=\"background: #ef233c; border: none; border-radius: 5px; padding: 5px; cursor: pointer; color: white;\" id=\"cancelButton\" onclick=\"document.getElementById('popuproot').remove();
        enableAll();\">
        Cancel
      </button>
    </div>`;

    popup("Create a new server")[1].innerHTML = popupContent;
}

function createServer() {
    const serverCreateName = document.getElementById("servercreatename").value;
    const serverCreatePort = document.getElementById("servercreateport").value;
    document.getElementById("popuproot").remove();
    enableAll();

    if (/\S/.test(serverCreateName)) {
        if (/\S/.test(serverCreatePort)) {
            fetch(
                `/api/addserver?name=${encodeURIComponent(
                    serverCreateName
                )}&port=${encodeURIComponent(serverCreatePort)}`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );
        }
    }

    updateServers();
}

updateServers();
setInterval(updateServers, 1000); // Adjust the interval as needed

const serverContent = document.getElementById("servercontent");

function deleteserver(id) {
    fetch(`/api/deleteserver?id=${id}`, { method: "DELETE" });
    document.getElementById("popuproot").remove();
    enableAll();
}

function deleteserverpropmpt(id) {
    const popupmenu = popup(`Are you sure you want to delete server #${id}`);
    popupmenu[1].innerHTML = `
    <div style="justify-content: center;margin-top: 20%;gap: 5px;display: flex;">
      <button style="
    background: #BDE363;
    border: none;
    border-radius: 5px;
    padding: 5px;
    cursor: pointer;
    color: white;
    font-size: 2em;
" onclick="deleteserver(${id})">Yes</button>
      <button style="
    background: #ef233c;
    border: none;
    border-radius: 5px;
    padding: 5px;
    cursor: pointer;
    color: white;
    font-size: 2em;
" onclick="document.getElementById('popuproot').remove();
        enableAll();">
        Cancel
      </button>
    </div>`;
}

function renameserver(id) {
    const newname = document.getElementById('serverrenamename').value
    document.getElementById('popuproot').remove();
    enableAll();

    if (/\S/.test(newname)) {        
        fetch(
            `/api/renameserver?name=${encodeURIComponent(newname)}&id=${id}`,
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
            }
        ).then(() => {
            window.location.reload()
        });
    }
}

function renameserverprompt(id) {
    const popupmenu = popup(`Renaming: #${id}`)

    popupmenu[1].innerHTML = `<label style="font-family: system-ui; color: white; margin-top: 10px; margin-left: 10px;">
      Name
    </label>
    <input type="text" id="serverrenamename" style="width: 50%; margin: 10px;">
    
    
    
    
    <div style="display: flex; justify-content: center; margin-top: 25px; gap: 5px;">
      <button style="background: #BDE363; border: none; border-radius: 5px; padding: 5px; cursor: pointer; color: white;" id="doneButtonRen" onclick="renameserver(${id});">
        Done
      </button>
      <button style="background: #ef233c; border: none; border-radius: 5px; padding: 5px; cursor: pointer; color: white;" id="cancelButton" onclick="document.getElementById('popuproot').remove();
        enableAll();">
        Cancel
      </button>
    </div>`
}

serverContent.addEventListener("contextmenu", (event) => {
    event.preventDefault();
    console.log("Right click detected on", event.target);
    console.log(event.target.getAttribute('server'))
    let contextmenu2 = contextmenu();
    contextmenu2.innerHTML = `
    <button id="renameserverbttn" onclick="renameserverprompt('${event.target.getAttribute(
        "server"
    )}')"><label class="material-symbols-rounded">edit</label>Rename server</button>
    
    <button id="managerserverbttn" onclick="alert('manage')"><label class="material-symbols-rounded">settings</label>Manage server</button>

    <button id="delserverbttn" onclick="deleteserverpropmpt('${event.target.getAttribute(
        "server"
    )}')"><label class="material-symbols-rounded">delete</label>Delete server</button>`;
});
