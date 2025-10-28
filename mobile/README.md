# AMIA Mobile App

A React Native mobile application built with Expo, TypeScript, and Redux Toolkit. This is the mobile version of the AMIA (Am I Available) web application.

## Features

- **Authentication**: Google OAuth integration with Supabase
- **Event Management**: Create, view, edit, and delete events
- **Relationship Management**: Manage connections with friends and family
- **Real-time Notifications**: Stay updated with relationship and event requests
- **Calendar Integration**: View and manage your schedule
- **Modern UI**: Clean, intuitive interface following the web app's design system

## Tech Stack

- **React Native** with Expo
- **TypeScript** for type safety
- **Redux Toolkit** for state management
- **React Navigation** for navigation
- **Supabase** for backend services
- **Expo Vector Icons** for icons

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- Expo CLI (`npm install -g @expo/cli`)
- iOS Simulator (for iOS development) or Android Studio (for Android development)

### Installation

1. Navigate to the mobile directory:
   ```bash
   cd mobile
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. **Configure Authentication (REQUIRED):**
   - The app is pre-configured with your Supabase credentials
   - **IMPORTANT:** Follow the [Infrastructure Setup Guide](./INFRASTRUCTURE_SETUP.md) to configure:
     - Supabase authentication settings
     - Google OAuth provider
     - Redirect URLs
     - RLS policies
   - Without proper configuration, authentication will not work

### Running the App

1. Start the development server:
   ```bash
   npm start
   ```

2. Run on specific platforms:
   ```bash
   # iOS
   npm run ios
   
   # Android
   npm run android
   
   # Web
   npm run web
   ```

## Project Structure

```
src/
├── api/                 # API layer
├── components/          # Reusable components
├── navigation/          # Navigation configuration
├── redux/              # Redux store and slices
├── screens/            # Screen components
├── types/              # TypeScript type definitions
└── lib/                # Utility libraries
```

## Key Features Implementation

### Authentication
- Google OAuth integration
- Session management with Supabase
- Protected routes and navigation

### State Management
- Redux Toolkit slices for:
  - Authentication
  - Relationships
  - Event Requests
  - Notifications
  - Calendar

### Navigation
- Stack navigation for main app flow
- Tab navigation for authenticated users
- Deep linking support

### UI Components
- Consistent design system matching web app
- Modern blue/purple color scheme
- Responsive layouts
- Touch-friendly interactions

## Development Notes

- The app follows the same patterns as the web client
- Redux state structure mirrors the web app
- API contracts are shared between web and mobile
- Styling uses React Native StyleSheet with consistent theming

## Building for Production

1. Configure app.json with production settings
2. Build for specific platforms:
   ```bash
   # iOS
   expo build:ios
   
   # Android
   expo build:android
   ```

## Contributing

1. Follow the existing code patterns
2. Use TypeScript for all new code
3. Follow the Redux patterns established in the web app
4. Test on both iOS and Android platforms