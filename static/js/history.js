document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('history-filters');
    const tableBody = document.getElementById('history-table-body');
    const pagination = document.getElementById('history-pagination');
    const activeFilters = document.getElementById('history-active-filters');
    const clearButton = document.getElementById('clear-history-filters');
    const cityFilter = document.getElementById('city-filter');
    const dateFilter = document.getElementById('date-filter');
    const historySection = document.getElementById('history');

    if (!form || !tableBody || !pagination) {
        return;
    }

    let currentPage = 1;
    let currentCity = cityFilter.value;
    let currentDate = dateFilter.value;

    function escapeHtml(value) {
        return String(value)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    function setLoading(isLoading) {
        tableBody.closest('.table-responsive')?.classList.toggle('is-loading', isLoading);
    }

    function updateUrl(page, city, date, pushState = true) {
        const params = new URLSearchParams(window.location.search);

        if (page > 1) {
            params.set('page', String(page));
        } else {
            params.delete('page');
        }

        if (city) {
            params.set('city', city);
        } else {
            params.delete('city');
        }

        if (date) {
            params.set('date', date);
        } else {
            params.delete('date');
        }

        const query = params.toString();
        const newUrl = query ? `/?${query}#history` : '/#history';

        if (pushState) {
            history.pushState({ page, city, date }, '', newUrl);
        }
    }

    function renderActiveFilters(city, date) {
        if (!activeFilters) {
            return;
        }

        if (!city && !date) {
            activeFilters.hidden = true;
            activeFilters.innerHTML = '';
            if (clearButton) {
                clearButton.hidden = true;
            }
            return;
        }

        activeFilters.hidden = false;
        if (clearButton) {
            clearButton.hidden = false;
        }

        const chips = [];
        if (city) {
            chips.push(`
                <span class="filter-chip">
                    <i class="bi bi-geo-alt"></i>
                    ${escapeHtml(city)}
                </span>
            `);
        }
        if (date) {
            chips.push(`
                <span class="filter-chip">
                    <i class="bi bi-calendar3"></i>
                    ${escapeHtml(date)}
                </span>
            `);
        }

        activeFilters.innerHTML = `
            <span class="active-filters__label">Đang lọc:</span>
            ${chips.join('')}
        `;
    }

    function renderTable(rows, hasFilters) {
        if (!rows.length) {
            const message = hasFilters
                ? 'Không có dữ liệu phù hợp với bộ lọc.'
                : 'Chưa có lịch sử dữ liệu.';
            tableBody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center text-muted py-4">${message}</td>
                </tr>
            `;
            return;
        }

        tableBody.innerHTML = rows.map((row) => `
            <tr>
                <td>
                    <span class="table-city">
                        <i class="bi bi-geo-alt-fill"></i>
                        ${escapeHtml(row.city)}
                    </span>
                </td>
                <td>${escapeHtml(row.temperature)} °C</td>
                <td>${escapeHtml(row.humidity)} %</td>
                <td>${escapeHtml(row.wind_speed)} m/s</td>
                <td>${escapeHtml(row.observation_time)}</td>
            </tr>
        `).join('');
    }

    function renderPagination(page, totalPages, city, date) {
        if (totalPages <= 1) {
            pagination.hidden = true;
            pagination.innerHTML = '';
            return;
        }

        pagination.hidden = false;

        const items = [];
        if (page > 1) {
            items.push(`
                <li class="page-item">
                    <a class="page-link" href="#" data-page="${page - 1}">
                        <i class="bi bi-chevron-left"></i>
                        Previous
                    </a>
                </li>
            `);
        }

        for (let pageNumber = 1; pageNumber <= totalPages; pageNumber += 1) {
            items.push(`
                <li class="page-item ${pageNumber === page ? 'active' : ''}">
                    <a class="page-link" href="#" data-page="${pageNumber}">${pageNumber}</a>
                </li>
            `);
        }

        if (page < totalPages) {
            items.push(`
                <li class="page-item">
                    <a class="page-link" href="#" data-page="${page + 1}">
                        Next
                        <i class="bi bi-chevron-right"></i>
                    </a>
                </li>
            `);
        }

        pagination.innerHTML = items.join('');
    }

    async function loadHistory(page = 1, city = '', date = '', pushState = true) {
        currentPage = page;
        currentCity = city;
        currentDate = date;

        cityFilter.value = city;
        dateFilter.value = date;

        setLoading(true);

        try {
            const params = new URLSearchParams({ page: String(page) });
            if (city) {
                params.set('city', city);
            }
            if (date) {
                params.set('date', date);
            }

            const response = await fetch(`/api/history?${params.toString()}`);
            if (!response.ok) {
                throw new Error('Không tải được lịch sử');
            }

            const data = await response.json();
            const hasFilters = Boolean(data.selected_city || data.selected_date);

            renderTable(data.history, hasFilters);
            renderPagination(data.page, data.total_pages, data.selected_city, data.selected_date);
            renderActiveFilters(data.selected_city, data.selected_date);
            updateUrl(data.page, data.selected_city, data.selected_date, pushState);

            if (historySection) {
                historySection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        } catch (error) {
            console.error(error);
            tableBody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center text-danger py-4">
                        Không thể tải dữ liệu. Vui lòng thử lại.
                    </td>
                </tr>
            `;
        } finally {
            setLoading(false);
        }
    }

    function readStateFromUrl() {
        const params = new URLSearchParams(window.location.search);
        return {
            page: Number(params.get('page') || 1),
            city: params.get('city') || '',
            date: params.get('date') || '',
        };
    }

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        loadHistory(1, cityFilter.value, dateFilter.value);
    });

    if (clearButton) {
        clearButton.addEventListener('click', (event) => {
            event.preventDefault();
            loadHistory(1, '', '');
        });
    }

    pagination.addEventListener('click', (event) => {
        const link = event.target.closest('[data-page]');
        if (!link) {
            return;
        }

        event.preventDefault();
        loadHistory(
            Number(link.dataset.page),
            currentCity,
            currentDate,
        );
    });

    window.addEventListener('popstate', (event) => {
        const state = event.state || readStateFromUrl();
        loadHistory(state.page || 1, state.city || '', state.date || '', false);
    });

    if (window.location.hash === '#history') {
        const initialState = readStateFromUrl();
        if (initialState.city || initialState.date || initialState.page > 1) {
            loadHistory(initialState.page, initialState.city, initialState.date, false);
        }
    }
});
