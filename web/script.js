const socket = io('http://localhost:80');

socket.on('connect', () => {
    console.log('Recived connect message, connected established!')
})

socket.on('memory', (data) => {
    document.getElementById('ramtext').innerHTML = Math.round(data / 2) + ' MiB'
})

socket.on('diskusage', (data) => {
    document.getElementById('disktext').innerHTML = data
})

function requestNewStats() {
    socket.emit('requestmem')
    socket.emit('requestdisk')
}
requestNewStats()

setInterval(requestNewStats, 500)