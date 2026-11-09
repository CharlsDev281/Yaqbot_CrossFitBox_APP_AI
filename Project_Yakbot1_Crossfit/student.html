const STORAGE_KEYS = {
  credentials: 'crossfit_box_credentials',
  workout: 'crossfit_box_workout',
  loggedIn: 'crossfit_box_logged_in'
};

const DEFAULT_CREDENTIALS = {
  userDomain: '@yaqbot.com',
  password: 'cookiesGalletaDelicious34'
};

function getWorkoutApiUrl() {
  const apiBaseUrl = (window.CROSSFIT_API_URL || '').trim().replace(/\/+$/, '');
  if (apiBaseUrl) {
    return `${apiBaseUrl}/api/workout`;
  }

  if (window.location.hostname.endsWith('github.io')) {
    throw new Error('Shared API is not configured. Set CROSSFIT_API_URL in config.js to your Render service URL.');
  }

  return '/api/workout';
}

function ensureCredentials() {
  const saved = localStorage.getItem(STORAGE_KEYS.credentials);

  if (!saved) {
    localStorage.setItem(STORAGE_KEYS.credentials, JSON.stringify(DEFAULT_CREDENTIALS));
    return DEFAULT_CREDENTIALS;
  }

  try {
    const parsed = JSON.parse(saved);
    const credentials = {
      userDomain: DEFAULT_CREDENTIALS.userDomain,
      password: parsed.password || DEFAULT_CREDENTIALS.password
    };
    localStorage.setItem(STORAGE_KEYS.credentials, JSON.stringify(credentials));
    return credentials;
  } catch (error) {
    localStorage.setItem(STORAGE_KEYS.credentials, JSON.stringify(DEFAULT_CREDENTIALS));
    return DEFAULT_CREDENTIALS;
  }
}

function isValidTeacherEmail(email) {
  return /^[^\s@]+@yaqbot\.com$/i.test(email);
}

function saveWorkoutState(workout) {
  localStorage.setItem(STORAGE_KEYS.workout, JSON.stringify(workout));
  return Promise.resolve().then(function () {
    return fetch(getWorkoutApiUrl(), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(workout)
    });
  }).then(function (response) {
    if (!response.ok) {
      throw new Error(`Workout sync failed (HTTP ${response.status})`);
    }
    window.dispatchEvent(new Event('workout-sync-success'));
  }).catch(function (error) {
    window.dispatchEvent(new CustomEvent('workout-sync-error', { detail: error }));
  });
}

function clearWorkoutState() {
  localStorage.removeItem(STORAGE_KEYS.workout);
  return Promise.resolve().then(function () {
    return fetch(getWorkoutApiUrl(), { method: 'DELETE' });
  }).then(function (response) {
    if (!response.ok) {
      throw new Error(`Workout reset failed (HTTP ${response.status})`);
    }
    window.dispatchEvent(new Event('workout-sync-success'));
  }).catch(function (error) {
    window.dispatchEvent(new CustomEvent('workout-sync-error', { detail: error }));
  });
}

function fetchSharedWorkoutState() {
  return Promise.resolve().then(function () {
    return fetch(getWorkoutApiUrl(), { cache: 'no-store' });
  }).then(function (response) {
    if (!response.ok) {
      throw new Error(`Workout sync failed (HTTP ${response.status})`);
    }
    return response.json().then(function (data) {
      return data.workout;
    });
  });
}

function cacheWorkoutState(workout) {
  if (workout === null) {
    localStorage.removeItem(STORAGE_KEYS.workout);
    return;
  }
  localStorage.setItem(STORAGE_KEYS.workout, JSON.stringify(workout));
}

function getWorkoutState() {
  const raw = localStorage.getItem(STORAGE_KEYS.workout);
  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw);
  } catch (error) {
    return null;
  }
}

function formatSeconds(totalSeconds) {
  const safeSeconds = Math.max(0, Number(totalSeconds) || 0);
  const minutes = Math.floor(safeSeconds / 60);
  const seconds = safeSeconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}
