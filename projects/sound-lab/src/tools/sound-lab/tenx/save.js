// Save straight into a chosen folder (File System Access API, Chrome/Edge/Arc) instead of ~/Downloads.
// The folder handle lives in IndexedDB so it survives reloads; the browser re-asks permission once per session.
import { downloadBlob } from '../../background-studio/utils/download';

const DB = 'sound-lab-10x';
const STORE = 'handles';
const KEY = 'folder';

export const canPickFolder = () => typeof window.showDirectoryPicker === 'function';

const db = () =>
  new Promise((resolve, reject) => {
    const request = indexedDB.open(DB, 1);
    request.onupgradeneeded = () => request.result.createObjectStore(STORE);
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });

const transact = async (mode, run) => {
  const database = await db();
  return new Promise((resolve, reject) => {
    const request = run(database.transaction(STORE, mode).objectStore(STORE));
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
};

export const loadFolder = () => transact('readonly', store => store.get(KEY)).catch(() => null);

export async function pickFolder() {
  const handle = await window.showDirectoryPicker({ id: 'sound-lab', mode: 'readwrite' });
  await transact('readwrite', store => store.put(handle, KEY));
  return handle;
}

export const forgetFolder = () => transact('readwrite', store => store.delete(KEY)).catch(() => null);

const writable = async handle => {
  if (!handle) return false;
  const options = { mode: 'readwrite' };
  if ((await handle.queryPermission(options)) === 'granted') return true;
  return (await handle.requestPermission(options)) === 'granted';
};

// files: [{ name, data: Blob|string }]. Into `folder/sub/` when a folder is set, else one download each
// (or `fallback()` when given, e.g. to zip them).
export async function saveFiles(folder, files, { sub = '', fallback = null } = {}) {
  if (folder && (await writable(folder).catch(() => false))) {
    const target = sub ? await folder.getDirectoryHandle(sub, { create: true }) : folder;
    for (const file of files) {
      const stream = await (await target.getFileHandle(file.name, { create: true })).createWritable();
      await stream.write(file.data);
      await stream.close();
    }
    return `${folder.name}${sub ? `/${sub}` : ''}`;
  }
  if (fallback) return fallback();
  files.forEach(file =>
    downloadBlob(typeof file.data === 'string' ? new Blob([file.data], { type: 'text/plain' }) : file.data, file.name)
  );
  return 'Downloads';
}
