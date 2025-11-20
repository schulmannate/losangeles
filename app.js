document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.content');
    const searchInput = document.getElementById('neighborhoodSearch');
    const clearBtn = document.getElementById('clearSearch');
    const alphabetNav = document.getElementById('alphabetNav');
    const loading = document.getElementById('loading');

    // State
    let currentData = neighborhoodData;
    let activeRegion = null;

    // Extract unique regions for filter
    const regions = [...new Set(neighborhoodData.map(item => item.region).filter(Boolean))].sort();

    // Create Filter UI
    const filterContainer = document.createElement('div');
    filterContainer.className = 'filter-container';
    filterContainer.innerHTML = `
        <div class="filter-scroll">
            <button class="filter-chip active" data-region="all">All Regions</button>
            ${regions.map(region => `<button class="filter-chip" data-region="${region}">${region}</button>`).join('')}
        </div>
    `;

    // Insert filter after search
    document.querySelector('.search-container').after(filterContainer);

    // Add styles for filters dynamically
    const style = document.createElement('style');
    style.textContent = `
        .filter-container {
            margin-bottom: 2rem;
            overflow-x: auto;
            padding-bottom: 0.5rem;
            -webkit-overflow-scrolling: touch;
        }
        .filter-scroll {
            display: flex;
            gap: 0.5rem;
            min-width: min-content;
        }
        .filter-chip {
            padding: 0.5rem 1rem;
            border: 1px solid var(--border-color);
            border-radius: 2rem;
            background: white;
            color: var(--text-secondary);
            cursor: pointer;
            white-space: nowrap;
            transition: var(--transition);
            font-size: 0.9rem;
            font-weight: 500;
        }
        .filter-chip:hover {
            background: var(--surface);
            border-color: var(--primary-color);
        }
        .filter-chip.active {
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }
        .no-results {
            text-align: center;
            padding: 4rem;
            color: var(--text-secondary);
        }
        .count-badge {
            display: inline-block;
            background: var(--surface);
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-left: 0.5rem;
            vertical-align: middle;
        }
        .hover-image-container {
            position: relative;
            cursor: pointer;
        }
        .hover-image {
            display: none;
            position: absolute;
            top: 100%;
            left: 0;
            z-index: 10;
            max-width: 300px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            margin-top: 0.5rem;
            border: 1px solid var(--border-color);
            background: white;
            padding: 4px;
        }
        .hover-image-container:hover .hover-image {
            display: block;
            animation: fadeIn 0.2s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-5px); }
            to { opacity: 1; transform: translateY(0); }
        }
    `;
    document.head.appendChild(style);

    // Render Function
    function render(data) {
        container.innerHTML = '';

        if (data.length === 0) {
            container.innerHTML = `
                <div class="no-results">
                    <h3>No neighborhoods found</h3>
                    <p>Try adjusting your search or filters</p>
                </div>
            `;
            return;
        }

        // Group by First Letter
        const grouped = data.reduce((acc, item) => {
            const letter = item.name.charAt(0).toUpperCase();
            if (!acc[letter]) acc[letter] = [];
            acc[letter].push(item);
            return acc;
        }, {});

        const letters = Object.keys(grouped).sort();

        letters.forEach(letter => {
            const section = document.createElement('section');
            section.id = `${letter.toLowerCase()}-section`;
            section.className = 'alphabet-section';

            const header = document.createElement('div');
            header.className = 'alphabet-letter';
            header.textContent = letter;
            section.appendChild(header);

            grouped[letter].forEach(item => {
                const card = document.createElement('article');
                card.className = 'neighborhood-card';
                card.dataset.region = item.region;

                // Header (Always visible)
                const header = document.createElement('div');
                header.className = 'neighborhood-header';
                header.innerHTML = `
                    <h2>${item.name}</h2>
                    <svg class="toggle-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                `;

                // Content (Hidden by default)
                const content = document.createElement('div');
                content.className = 'neighborhood-content';

                const details = document.createElement('div');
                details.className = 'neighborhood-details';

                let detailsHtml = '';

                if (item.description) {
                    detailsHtml += `<div class="description">${item.description}</div>`;
                }

                if (item.subAreas) {
                    detailsHtml += `<div class="sub-areas">${item.subAreas}</div>`;
                }

                if (item.region) {
                    detailsHtml += `<span class="region">${item.region}</span>`;
                }

                details.innerHTML = detailsHtml;
                content.appendChild(details);

                card.appendChild(header);
                card.appendChild(content);
                section.appendChild(card);

                // Toggle Event
                header.addEventListener('click', () => {
                    const isExpanded = card.classList.contains('expanded');

                    // Optional: Close others when opening one (Accordion style)
                    // document.querySelectorAll('.neighborhood-card.expanded').forEach(c => {
                    //     if (c !== card) c.classList.remove('expanded');
                    // });

                    card.classList.toggle('expanded');
                });
            });

            container.appendChild(section);
        });

        // Update Alphabet Nav State
        document.querySelectorAll('.alphabet-nav a').forEach(link => {
            const letter = link.textContent;
            if (letters.includes(letter)) {
                link.classList.remove('disabled');
                link.style.opacity = '1';
                link.style.pointerEvents = 'auto';
            } else {
                link.classList.add('disabled');
                link.style.opacity = '0.3';
                link.style.pointerEvents = 'none';
            }
        });
    }

    // Filter Function
    function filterData() {
        const searchTerm = searchInput.value.toLowerCase();

        const filtered = neighborhoodData.filter(item => {
            const matchesSearch = item.name.toLowerCase().includes(searchTerm) ||
                (item.description && item.description.toLowerCase().includes(searchTerm)) ||
                (item.subAreas && item.subAreas.toLowerCase().includes(searchTerm));

            const matchesRegion = activeRegion === 'all' || !activeRegion || item.region === activeRegion;

            return matchesSearch && matchesRegion;
        });

        render(filtered);

        // Show clear button if search has text
        clearBtn.style.display = searchTerm ? 'flex' : 'none';
    }

    // Event Listeners
    searchInput.addEventListener('input', filterData);

    clearBtn.addEventListener('click', () => {
        searchInput.value = '';
        filterData();
        searchInput.focus();
    });

    // Region Filter Click
    filterContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('filter-chip')) {
            // Update UI
            document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
            e.target.classList.add('active');

            // Update State
            activeRegion = e.target.dataset.region;
            filterData();
        }
    });

    // Initial Render
    render(neighborhoodData);

    // Hide loading
    if (loading) {
        loading.classList.add('hidden');
        setTimeout(() => loading.remove(), 500);
    }
});
