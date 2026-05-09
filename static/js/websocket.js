// WebSocket connection and event handling
const socket = io();

socket.on('connection_response', function(data) {
    console.log('WebSocket connected:', data);
});

socket.on('task_update', function(data) {
    console.log('Task update received:', data);
    // Emit event that can be listened to by other components
    window.dispatchEvent(new CustomEvent('taskUpdated', { detail: data }));
});

socket.on('task_update', function(data) {
    console.log('Real-time task update:', data);
});

socket.on('notifications', function(data) {
    console.log('Notifications:', data);
    // Update notification count in UI if needed
});

socket.on('disconnect', function() {
    console.log('WebSocket disconnected');
});
