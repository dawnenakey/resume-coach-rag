document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.querySelector('.upload-form');
    const fileInput = document.querySelector('#resume-file');
    const loadingIndicator = document.querySelector('.loading');
    const resultsSection = document.querySelector('.results');

    function showLoading() {
        loadingIndicator.classList.add('active');
    }

    function hideLoading() {
        loadingIndicator.classList.remove('active');
    }

    function showAlert(message, type = 'error') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;
        
        // Remove any existing alerts
        document.querySelectorAll('.alert').forEach(alert => alert.remove());
        
        // Insert the new alert at the top of the form
        uploadForm.insertBefore(alertDiv, uploadForm.firstChild);
        
        // Auto-remove the alert after 5 seconds
        setTimeout(() => alertDiv.remove(), 5000);
    }

    function displayResults(data) {
        // Clear previous results
        resultsSection.innerHTML = '';

        // Create metrics section
        const metricsDiv = document.createElement('div');
        metricsDiv.className = 'metrics';

        // Add metric cards
        const metrics = [
            { label: 'Overall Score', value: data.score },
            { label: 'Keywords Match', value: `${data.keywordMatch}%` },
            { label: 'Readability', value: data.readability },
            { label: 'Experience Level', value: data.experienceLevel }
        ];

        metrics.forEach(metric => {
            const metricCard = document.createElement('div');
            metricCard.className = 'metric-card';
            metricCard.innerHTML = `
                <div class="metric-value">${metric.value}</div>
                <div class="metric-label">${metric.label}</div>
            `;
            metricsDiv.appendChild(metricCard);
        });

        // Add suggestions section
        const suggestionsDiv = document.createElement('div');
        suggestionsDiv.className = 'suggestions';
        suggestionsDiv.innerHTML = `
            <h3>Improvement Suggestions</h3>
            <ul>
                ${data.suggestions.map(suggestion => `<li>${suggestion}</li>`).join('')}
            </ul>
        `;

        // Add visualization section (placeholder for charts)
        const visualizationDiv = document.createElement('div');
        visualizationDiv.className = 'visualization';
        visualizationDiv.innerHTML = `
            <h3>Skills Analysis</h3>
            <div class="chart-container">
                <!-- Chart will be inserted here -->
            </div>
        `;

        // Append all sections to results
        resultsSection.appendChild(metricsDiv);
        resultsSection.appendChild(suggestionsDiv);
        resultsSection.appendChild(visualizationDiv);

        // Show results section
        resultsSection.style.display = 'block';
    }

    async function handleSubmit(event) {
        event.preventDefault();
        
        const formData = new FormData();
        const file = fileInput.files[0];

        if (!file) {
            showAlert('Please select a resume file to analyze');
            return;
        }

        formData.append('resume', file);

        try {
            showLoading();
            
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Failed to analyze resume');
            }

            const data = await response.json();
            hideLoading();
            displayResults(data);
            showAlert('Resume analysis completed successfully', 'success');
        } catch (error) {
            hideLoading();
            showAlert(error.message);
            console.error('Error:', error);
        }
    }

    // Event listeners
    uploadForm.addEventListener('submit', handleSubmit);

    // File input change handler to show selected filename
    fileInput.addEventListener('change', (e) => {
        const fileName = e.target.files[0]?.name;
        const fileLabel = document.querySelector('.file-label');
        if (fileLabel) {
            fileLabel.textContent = fileName || 'Choose a file';
        }
    });
}); 