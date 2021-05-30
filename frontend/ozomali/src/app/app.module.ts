import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { MatNativeDateModule, MatRippleModule, MAT_DATE_LOCALE } from '@angular/material/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ComponentsModule } from './components/components.module';
import { DefaultScreenComponent } from './pages/default-screen/default-screen.component';
import { VendorScreenComponent } from './pages/vendor-screen/vendor-screen.component';
import { ProductScreenComponent } from './pages/product-screen/product-screen.component';
import { LoginScreenComponent } from './pages/login-screen/login-screen.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatMenuModule } from '@angular/material/menu';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { NgxMaskModule } from 'ngx-mask';
import { MatTabsModule } from '@angular/material/tabs';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { AuthInterceptor } from './interceptors/auth.interceptor';
import { MovingsScreenComponent } from './pages/movings-screen/movings-screen.component';
import { CurrencyMaskConfig, CURRENCY_MASK_CONFIG } from 'ng2-currency-mask';
import { ChartsModule } from 'ng2-charts';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { DatePipe } from '@angular/common';
import { ReportScreenComponent } from './pages/report-screen/report-screen.component';

export const currencyMaskConfig: CurrencyMaskConfig = {
  align: 'left',
  allowNegative: false,
  decimal: ',',
  precision: 2,
  prefix: 'R$ ',
  suffix: '',
  thousands: '.',
};

@NgModule({
  declarations: [
    AppComponent,
    DefaultScreenComponent,
    VendorScreenComponent,
    ProductScreenComponent,
    LoginScreenComponent,
    MovingsScreenComponent,
    ReportScreenComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    ComponentsModule,
    MatRippleModule,
    FormsModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatMenuModule,
    HttpClientModule,
    NgxMaskModule.forRoot(),
    MatTabsModule,
    MatProgressSpinnerModule,
    ChartsModule,
    MatNativeDateModule,
    MatDatepickerModule,
    MatButtonModule,
    MatSelectModule,
  ],
  providers: [
    MatDatepickerModule,
    DatePipe,
    { provide: CURRENCY_MASK_CONFIG, useValue: currencyMaskConfig },
    { provide: MAT_DATE_LOCALE, useValue: 'pt-BR' },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true,
    },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
