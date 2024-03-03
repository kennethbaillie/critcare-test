
Display name:
guidelines_app

Application (client) ID:
8e7f0686-16f5-4943-99a1-572be2625549

Object ID:
37c91a00-9a96-42a8-8734-79df8721ac22

Directory (tenant) ID:
2e9f06b0-1669-4589-8789-10a06934dc61


client secret - expires 2025-04-28
syw8Q~k4jGjbDJv4sDc6XjbjqON3PO3XndXwBacS

client secret id:
de8b9219-f311-43ed-be15-3255548462ba



# Instructions for NHS IT

To register an app on Azure to access OneDrive through Microsoft Graph API, follow these steps:

Go to the Azure portal.
Sign in with your Microsoft account.
In the left sidebar, click on "Azure Active Directory."
In the Azure Active Directory overview, click on "App registrations."
Click on the "New registration" button.
Enter a name for your app, such as "OneDriveDownloader."
Choose the supported account types (usually "Accounts in any organizational directory (Any Azure AD directory - Multitenant) and personal Microsoft accounts (e.g., Skype, Xbox)").
Leave the "Redirect URI" section blank for now. Click on the "Register" button.
You will be redirected to the app's overview page. Copy the "Application (client) ID" and "Directory (tenant) ID" values; you'll need them later.
Next, you need to create a client secret for your app:

In the app's left sidebar, click on "Certificates & secrets."
Click on the "New client secret" button.
Enter a description for the client secret and choose an expiration period. Click on "Add."
Copy the generated client secret value immediately, as you won't be able to see it again.
Finally, you need to grant your app the necessary permissions to access OneDrive:

In the app's left sidebar, click on "API permissions."
Click on the "Add a permission" button.
Select "Microsoft Graph" in the "Request API permissions" panel.
Choose "Application permissions."
In the "Select permissions" search box, type "Files" and select the "Files.Read.All" permission.
Click on the "Add permissions" button.
To grant admin consent for the permissions, click on the "Grant admin consent for [Your Directory Name]" button and confirm the action.
Now you have registered an app on Azure with the necessary permissions to access OneDrive. Use the "Application (client) ID," "Directory (tenant) ID," and the client secret you generated to authenticate with the Microsoft Graph API in your Python script.



