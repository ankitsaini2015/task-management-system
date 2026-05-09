// Tasks functionality

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

function getPriorityColor(priority) {
    const colors = {
        'low': '#17a2b8',
        'medium': '#ffc107',
        'high': '#fd7e14',
        'urgent': '#dc3545'
    };
    return colors[priority] || '#999';
}

function getStatusBadge(status) {
    const statuses = {
        'pending': '⏳ Pending',
        'in_progress': '🔄 In Progress',
        'completed': '✅ Completed',
        'cancelled': '❌ Cancelled'
    };
    return statuses[status] || status;
}
