import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map, catchError, tap  } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class AuthGuardService implements CanActivate {
  private isAuthenticated: boolean | null = null; // Cache authentication status

  constructor(private router: Router, private http: HttpClient) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> {

    if (this.isAuthenticated !== null) { 
      // If authentication status is cached, use it
      return of(this.isAuthenticated);
    }

    // Otherwise, make an API call to check authentication
    return this.isLoggedIn().pipe(
      tap((authStatus) => {
        this.isAuthenticated = authStatus; // Cache authentication status
      }),
      map((authStatus) => {
        if (authStatus) {
          return true;
        } else {
          this.router.navigate(['/login']);
          return false;
        }
      }),
      catchError((error) => {
        console.error('Error during authentication check:', error);
        this.router.navigate(['/login']);
        return of(false);
      })
    );
  }

  private isLoggedIn(): Observable<boolean> {
    return this.http
      .post<{ is_authenticated: boolean }>('https://taskmatesbackend-pd5h.onrender.com/api/accounts/check_authentication', {withCredentials: true})
      .pipe(
        map((response) => response.is_authenticated),
        catchError((error) => {
          console.error('Authentication check failed:', error);
          return of(false);
        })
      );
  }

  // Add a logout method to clear the cache when needed
  public logout(): void {
    this.isAuthenticated = null;
  }
}
