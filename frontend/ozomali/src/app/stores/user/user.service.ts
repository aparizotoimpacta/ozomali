import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { UserStore } from './user.store';

@Injectable({ providedIn: 'root' })
export class UserService {
  private readonly baseUrl: string;

  constructor(private userStore: UserStore, private http: HttpClient) {
    this.baseUrl = 'https://ozomali-api.herokuapp.com/api/v1/auth';
  }

  login(params: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/login`, params);
  }

  updateAuthentication(isAuthenticated: boolean, token: string, user: any): void {
    this.userStore.update({ isAuthenticated, token, user });
  }

  logout(): void {
    this.userStore.reset();
  }
}
