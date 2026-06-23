// Direct SQLite seed script - no API auth needed
const Database = require('better-sqlite3');
const path = require('path');

const dbPath = path.join(__dirname, '.tmp', 'data.db');
const db = new Database(dbPath);

console.log('Connected to SQLite database');

// Helper: generate a random document ID (Strapi 5 format)
function docId() {
  const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
  let id = '';
  for (let i = 0; i < 22; i++) id += chars[Math.floor(Math.random() * chars.length)];
  return id;
}

const now = new Date().toISOString();

// Check existing tables
const tables = db.prepare("SELECT name FROM sqlite_master WHERE type='table'").all();
console.log('Tables:', tables.map(t => t.name).join(', '));

// Find the category table
const catTables = tables.filter(t => t.name.includes('category') && !t.name.includes('components') && !t.name.includes('links'));
console.log('Category tables:', catTables.map(t => t.name));

// Check category table schema
if (catTables.length > 0) {
  const schema = db.prepare(`PRAGMA table_info('${catTables[0].name}')`).all();
  console.log('Category schema:', schema.map(c => c.name).join(', '));
}

db.close();
console.log('Done');
