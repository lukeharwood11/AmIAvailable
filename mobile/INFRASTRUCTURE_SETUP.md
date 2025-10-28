# AMIA Mobile App - Infrastructure Setup Guide

This guide covers all the infrastructure changes needed to get the mobile app authentication working with Supabase and Google OAuth.

## 🔧 Supabase Dashboard Configuration

### 1. Authentication Settings

1. **Go to Supabase Dashboard** → Your Project → Authentication → Settings

2. **Configure Site URL:**
   ```
   https://cwpsafmbigglcsbpwawr.supabase.co
   ```

3. **Configure Redirect URLs:**
   Add these URLs to the "Redirect URLs" section:
   ```
   am-i-available://auth/callback
   exp://192.168.1.100:8081/--/auth/callback
   exp://localhost:8081/--/auth/callback
   ```

4. **Configure Additional Redirect URLs for Development:**
   ```
   exp://127.0.0.1:8081/--/auth/callback
   exp://10.0.2.2:8081/--/auth/callback
   ```

### 2. Google OAuth Provider Setup

1. **Go to Authentication → Providers → Google**

2. **Enable Google Provider:**
   - Toggle "Enable Google provider" to ON

3. **Configure Google OAuth:**
   - **Client ID:** (Get from Google Console - see below)
   - **Client Secret:** (Get from Google Console - see below)

### 3. RLS (Row Level Security) Policies

Ensure your existing RLS policies are configured for the mobile app. The policies should allow:
- Users to access their own data
- Proper authentication checks
- Mobile app user access

## 🔑 Google Cloud Console Configuration

### 1. Create/Configure OAuth 2.0 Credentials

1. **Go to Google Cloud Console:**
   - Navigate to [Google Cloud Console](https://console.cloud.google.com/)
   - Select your project or create a new one

2. **Enable Google+ API:**
   - Go to "APIs & Services" → "Library"
   - Search for "Google+ API" and enable it
   - Also enable "Google People API" for user profile access

3. **Create OAuth 2.0 Credentials:**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth 2.0 Client IDs"

4. **Configure OAuth Consent Screen:**
   - Go to "OAuth consent screen"
   - Choose "External" user type
   - Fill in required fields:
     - App name: "AMIA Mobile"
     - User support email: your email
     - Developer contact: your email
   - Add scopes:
     - `../auth/userinfo.email`
     - `../auth/userinfo.profile`
     - `../auth/calendar.readonly` (if needed for calendar integration)

### 2. Configure OAuth Client

1. **Application Type:** Web application

2. **Authorized JavaScript origins:**
   ```
   https://cwpsafmbigglcsbpwawr.supabase.co
   ```

3. **Authorized redirect URIs:**
   ```
   https://cwpsafmbigglcsbpwawr.supabase.co/auth/v1/callback
   ```

4. **For Development (Expo):**
   Add these additional redirect URIs:
   ```
   exp://192.168.1.100:8081/--/auth/callback
   exp://localhost:8081/--/auth/callback
   exp://127.0.0.1:8081/--/auth/callback
   exp://10.0.2.2:8081/--/auth/callback
   ```

### 3. Get Credentials

After creating the OAuth client:
1. Copy the **Client ID**
2. Copy the **Client Secret**
3. Add these to your Supabase Google provider configuration

## 📱 Mobile App Configuration

### 1. Environment Variables

The app is already configured with your Supabase credentials in `app.json`:

```json
{
  "expo": {
    "extra": {
      "supabaseUrl": "https://cwpsafmbigglcsbpwawr.supabase.co",
      "supabaseAnonKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3cHNhZm1iaWdnbGNzYnB3YXdyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcxNzIyMDAsImV4cCI6MjA3Mjc0ODIwMH0.8pe-ditIEk8aG9pYmknVP320Nqiwe0npYq2Ij6-lBW0"
    }
  }
}
```

### 2. Deep Linking Configuration

The app is configured with the scheme `am-i-available://` for deep linking.

## 🚀 Testing the Setup

### 1. Start the Development Server

```bash
cd mobile
npm install
npm start
```

### 2. Test Authentication Flow

1. **Run on iOS Simulator:**
   ```bash
   npm run ios
   ```

2. **Run on Android Emulator:**
   ```bash
   npm run android
   ```

3. **Test the flow:**
   - Tap "Get Started" on landing screen
   - Tap "Continue with Google" on login screen
   - Complete Google OAuth flow
   - Should redirect back to app and show authenticated state

### 3. Debug Authentication Issues

If authentication fails, check:

1. **Supabase Logs:**
   - Go to Supabase Dashboard → Logs
   - Look for authentication errors

2. **Expo Logs:**
   ```bash
   npx expo logs
   ```

3. **Common Issues:**
   - Redirect URLs not properly configured
   - Google OAuth credentials not set in Supabase
   - RLS policies blocking access
   - Network connectivity issues

## 🔒 Security Considerations

### 1. Production Configuration

For production deployment:

1. **Update Redirect URLs:**
   - Remove development URLs
   - Add production app URLs
   - Configure proper app store URLs

2. **Environment Variables:**
   - Use environment-specific Supabase projects
   - Secure credential storage
   - Enable proper RLS policies

3. **App Store Configuration:**
   - Configure proper URL schemes
   - Set up universal links (iOS)
   - Configure app links (Android)

### 2. RLS Policies

Ensure your RLS policies allow:
```sql
-- Example policy for user_tokens table
CREATE POLICY "Users can access own tokens" ON user_tokens
FOR ALL USING (auth.uid() = id);

-- Example policy for relationships table
CREATE POLICY "Users can access own relationships" ON relationships
FOR ALL USING (auth.uid() = user_id_1 OR auth.uid() = user_id_2);
```

## 📋 Checklist

- [ ] Supabase redirect URLs configured
- [ ] Google OAuth provider enabled in Supabase
- [ ] Google Cloud Console OAuth credentials created
- [ ] OAuth consent screen configured
- [ ] Redirect URIs added to Google OAuth client
- [ ] Supabase Google provider configured with Client ID and Secret
- [ ] RLS policies configured for mobile app
- [ ] Mobile app tested on iOS/Android
- [ ] Authentication flow working end-to-end

## 🆘 Troubleshooting

### Common Issues:

1. **"Invalid redirect URI" error:**
   - Check that all redirect URIs are properly configured in both Supabase and Google Console

2. **"OAuth consent screen" error:**
   - Ensure OAuth consent screen is properly configured in Google Console

3. **"RLS policy" errors:**
   - Check that RLS policies allow authenticated users to access their data

4. **Deep linking not working:**
   - Ensure the app scheme is properly configured
   - Test with `npx uri-scheme open am-i-available://auth/callback`

### Getting Help:

1. Check Supabase logs for detailed error messages
2. Use Expo debugging tools
3. Test with different redirect URI formats
4. Verify Google OAuth configuration matches Supabase settings