import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TranscriptionComponent } from './main/transcription/transcription.component';
import { SummaryComponent } from './main/summary/summary/summary.component';

const routes: Routes = [
  {path: 'transcription', component: TranscriptionComponent},
  {path: 'summary', component: SummaryComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
