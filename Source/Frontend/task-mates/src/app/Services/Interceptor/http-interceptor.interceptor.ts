import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class MyHttpInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Only proceed if we're in a browser environment
    if (typeof window !== 'undefined') {
      // Get the token from localStorage (if available)
      const token = localStorage.getItem('access_token'); // Assuming the token is stored here

      // Get the CSRF token (if required for Django or CSRF-protected backends)
      const csrfToken = document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken='));

      // Extract the value of the CSRF token if it exists
      const csrfValue = csrfToken ? csrfToken.split('=')[1] : '';

      // Clone the request to add the authorization header and CSRF token if they exist
      let modifiedReq = req;

      // Add Authorization header if token is available
      if (token) {
        modifiedReq = req.clone({
          setHeaders: {
            Authorization: `Bearer ${token}`
          }
        });
      }

      // Add CSRF token to headers if it's present
      if (csrfValue) {
        modifiedReq = modifiedReq.clone({
          setHeaders: {
            'X-CSRFToken': csrfValue // Add CSRF token for Django
          }
        });
      }

      // Proceed with the modified request
      return next.handle(modifiedReq);
    } else {
      // If not in a browser, just pass the request unchanged
      return next.handle(req);
    }
  }
}
