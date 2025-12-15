// Web Worker for FID optimization
// Handles heavy computations without blocking main thread

self.addEventListener('message', function(e) {
    const { type, data } = e.data;
    
    switch (type) {
        case 'PROCESS_DATA':
            // Simulate heavy data processing
            const result = processData(data);
            self.postMessage({
                type: 'DATA_PROCESSED',
                result: result
            });
            break;
            
        case 'CALCULATE_STATS':
            // Calculate statistics without blocking UI
            const stats = calculateStats(data);
            self.postMessage({
                type: 'STATS_CALCULATED',
                stats: stats
            });
            break;
            
        default:
            self.postMessage({
                type: 'ERROR',
                message: 'Unknown message type'
            });
    }
});

function processData(data) {
    // Heavy data processing logic
    return data.map(item => ({
        ...item,
        processed: true,
        timestamp: Date.now()
    }));
}

function calculateStats(data) {
    // Statistical calculations
    const sum = data.reduce((acc, item) => acc + (item.value || 0), 0);
    const avg = sum / data.length;
    const max = Math.max(...data.map(item => item.value || 0));
    const min = Math.min(...data.map(item => item.value || 0));
    
    return {
        sum,
        average: avg,
        max,
        min,
        count: data.length
    };
}
