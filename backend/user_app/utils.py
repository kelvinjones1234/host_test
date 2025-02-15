import requests
import base64
from django.core.cache import cache
from requests.exceptions import RequestException


from dotenv import load_dotenv
import os

# Load environme
load_dotenv()

class MonnifyAPIClient:
    """
    API client for interacting with Monnify's sandbox API
    """
    def __init__(self, 
                 api_key=None, 
                 secret_key=None):
        """
        Initialize Monnify API client
        
        :param api_key: Monnify API key
        :param secret_key: Monnify secret key
        """
        # Use settings if not provided directly
        self.api_key = os.getenv('MONIFY_API_KEY')
        self.secret_key = os.getenv('MONIFY_SECRETE_KEY')

        
        # Base URLs
        self.login_url = 'https://sandbox.monnify.com/api/v1/auth/login'
        self.base_api_url = 'https://sandbox.monnify.com/api/v2'
        
        # Cache key for access token
        self.token_cache_key = 'monnify_access_token'
    
    def _get_access_token(self):
        """
        Obtain access token from Monnify
        
        :return: Access token string
        :raises RequestException: If token retrieval fails
        """
        try:
            # Create base64 encoded credentials
            credentials = f"{self.api_key}:{self.secret_key}"
            encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
            print(encoded_credentials)
            
            # Prepare headers
            headers = {
                'Authorization': f'Basic {encoded_credentials}',
                'Content-Type': 'application/json'
            }
            
            # Make login request
            response = requests.post(
                self.login_url, 
                headers=headers
            )
            
            # Raise an exception for bad responses
            response.raise_for_status()
            
            # Extract access token from response
            response_data = response.json()
            
            # Check if response contains access token
            if not response_data.get('requestSuccessful', False):
                raise ValueError("Token retrieval failed")
            
            # Extract token and its details
            token_data = response_data.get('responseBody', {})
            access_token = token_data.get('accessToken')
            
            # Default expiration to 1 hour if not specified
            expires_in = 3600
            
            # Cache the token
            cache.set(self.token_cache_key, access_token, expires_in)
            
            return access_token
        
        except RequestException as e:
            print(f"Failed to obtain Monnify access token: {e}")
            raise
    
    def get_valid_token(self):
        """
        Retrieve a valid access token
        
        :return: Valid access token
        """
        # Try to get cached token first
        cached_token = cache.get(self.token_cache_key)
        if cached_token:
            return cached_token
        
        # If no cached token, get a new one
        return self._get_access_token()
    
    def create_reserved_account(self, account_details):
        """
        Create a reserved account via Monnify API
        
        :param account_details: Dictionary with account creation details
        :return: API response for reserved account creation
        """
        # Get valid access token
        access_token = self.get_valid_token()
        
        # Prepare request URL and headers
        url = f"{self.base_api_url}/bank-transfer/reserved-accounts/"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            # Make the API request
            response = requests.post(
                url, 
                headers=headers, 
                json=account_details
            )
            
            # Raise an exception for bad responses
            response.raise_for_status()
            
            # Return the response data
            return response.json()
        
        except RequestException as e:
            print(f"Failed to create reserved account: {e}")
            raise
