# Code RAG Search - Frontend

A modern React + Vite frontend for semantic code search powered by AI embeddings.

## Features

- 🔍 **Search Interface**: Intuitive search for code functionality
- 📦 **Database Management**: Easy GitHub repository processing
- ⚡ **Real-time Results**: Instant semantic search with similarity scoring
- 🎨 **Modern UI**: Professional, responsive design with beautiful components
- 📱 **Mobile Friendly**: Works seamlessly on all device sizes
- 🚀 **Fast Build**: Vite-powered fast development and builds

## Quick Start

### Prerequisites

- Node.js 16+ and npm (or yarn/pnpm)
- Backend API running on `http://localhost:8000`

### Installation

1. **Create environment configuration:**

```bash
cp .env.example .env
```

2. **Install dependencies:**

```bash
npm install
```

3. **Start development server:**

```bash
npm run dev
```

The frontend will open automatically at `http://localhost:3000`.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── RepoInput.jsx       # GitHub repo input form
│   │   ├── RepoInput.css       # Repo input styling
│   │   ├── SearchInput.jsx     # Search query form
│   │   ├── SearchInput.css     # Search input styling
│   │   ├── ResultsDisplay.jsx  # Results display component
│   │   └── ResultsDisplay.css  # Results styling
│   ├── services/
│   │   └── api.js              # Backend API wrapper with Axios
│   ├── App.jsx                 # Main orchestrating component
│   ├── App.css                 # App-level styling
│   ├── index.css               # Global styles and variables
│   └── main.jsx                # React entry point
├── index.html                  # HTML entry point
├── package.json                # Dependencies
├── vite.config.js              # Build configuration
├── .env.example                # Example environment variables
└── .gitignore                  # Git ignore rules
```

## Usage

### Building Database from GitHub

1. Enter the GitHub repository owner and name (e.g., `facebook/react`)
2. Optionally check "Force Rebuild" to reprocess existing repositories
3. Click "Build Database" to start processing
4. Wait for the status message showing the number of chunks processed

### Searching Code

1. After building a database, use the search input on the right
2. Enter a natural language query (e.g., "HTTP request handler", "authentication function")
3. Adjust the number of results (1-20) using the slider
4. Click "Search" or press Enter
5. View results with similarity scores and code previews

### Copy Code Snippets

- Hover over any result code block
- Click the "Copy" button to copy the code to clipboard
- Confirmation message appears when copied

## API Integration

The frontend connects to the following backend endpoints:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/build` | Build/rebuild database from GitHub repo |
| POST | `/search` | Semantic code search |
| GET | `/stats` | Get database statistics |
| GET | `/health` | Health check endpoint |

See [services/api.js](src/services/api.js) for implementation details.

## Configuration

### Environment Variables

- `VITE_API_URL`: Backend API base URL (default: `http://localhost:8000`)

### Styling Customization

Global CSS variables in [src/index.css](src/index.css):

```css
:root {
  --color-primary: #667eea;        /* Primary color (purple) */
  --color-secondary: #764ba2;      /* Secondary color */
  --color-success: #4caf50;        /* Success state (green) */
  --color-error: #f44336;          /* Error state (red) */
}
```

## Available Scripts

```bash
# Development server with HMR
npm run dev

# Production build
npm run build

# Preview production build locally
npm run preview

# Lint check (if configured)
npm run lint
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance Optimization

- **Code Splitting**: Vite automatically optimizes chunks
- **Lazy Loading**: Components load on demand
- **Asset Optimization**: Images and fonts are optimized
- **CSS Modules**: Scoped styling reduces conflicts

## Troubleshooting

### "Cannot find API" or Connection Error

- Ensure backend is running on `http://localhost:8000`
- Check `VITE_API_URL` in `.env` file
- Verify backend CORS configuration allows frontend origin

### Database Build Fails

- Ensure GitHub repository exists and is public
- Check GitHub token in backend configuration
- Try with a different repository
- Check browser console for detailed error messages

### Search Returns No Results

- Database may not be built yet
- Try a different search query
- Increase the number of results using the slider
- Rebuild the database with "Force Rebuild" option

### Slow Performance

- Check network speed and backend response time
- Clear browser cache
- Try with fewer results count initially
- Ensure backend is not processing multiple requests

## Development

### Adding New Components

1. Create component file in `src/components/`
2. Create corresponding `.css` file
3. Import and use in `App.jsx`

### Extending API Service

Add new methods to [src/services/api.js](src/services/api.js):

```javascript
export async function newEndpoint(params) {
  try {
    const response = await api.post('/endpoint', params);
    return response.data;
  } catch (error) {
    throw new Error(`Failed to call endpoint: ${error.message}`);
  }
}
```

## Deployment

### Build for Production

```bash
npm run build
```

This creates an optimized `dist/` folder.

### Deploy to Vercel

```bash
npm install -g vercel
vercel
```

### Deploy to Netlify

```bash
npm run build
netlify deploy --prod --dir=dist
```

### Deploy to Static Host (S3, GitHub Pages, etc.)

1. Run `npm run build`
2. Upload contents of `dist/` folder to your host
3. Configure backend URL in `.env` on the server

## Dependencies

- **React 18.2.0**: UI library
- **Vite 5.0.0**: Build tool and dev server
- **Axios 1.6.0**: HTTP client
- **React DOM 18.2.0**: React rendering

## License

This project is part of the Code RAG system (see backend repository for license details).

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Review backend logs for API errors
3. Check browser console for client-side errors
4. Ensure all environment variables are properly configured

## Next Steps

- Customize colors and styling to match your brand
- Add additional search filters
- Integrate with your development workflow
- Deploy to production server
