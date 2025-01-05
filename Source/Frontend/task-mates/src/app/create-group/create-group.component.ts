import { Component, OnInit } from '@angular/core';
import { GalleriaModule } from 'primeng/galleria';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';




@Component({
  selector: 'app-create-group',
  standalone: true,
  imports: [GalleriaModule, ReactiveFormsModule, HttpClientModule, ButtonModule, InputTextModule],
  templateUrl: './create-group.component.html',
  styleUrl: './create-group.component.css'
})
export class CreateGroupComponent {
  apiUrl = 'http://127.0.0.1:8000/api'; // Django API endpoints
  selectedImage: any | null = null;
  group: any;
  images: any[] = [];

  groupForm: FormGroup;
  base64Image: string = '';

  constructor(private fb: FormBuilder, private http: HttpClient, private router: Router) {
    this.loadImages();
    this.groupForm = this.fb.group({
      name: ['', Validators.required], // Group name is required
    });
  }


  responsiveOptions: any[] = [
      {
          breakpoint: '1300px',
          numVisible: 4,
      },
      {
          breakpoint: '575px',
          numVisible: 1,
      },
  ];

  onImageSelect(image: any) {
    if (this.selectedImage === image.previewImageSrc) {
        this.selectedImage = null; // Deselect the image
    } else {
        this.selectedImage = image.previewImageSrc; // Select the image
    }
    if (this.selectedImage) {
      this.convertToBase64(this.selectedImage); // Convert the selected image to Base64
    }
    console.log('Image selected:', this.selectedImage);
}

 
  
  convertToBase64(imageUrl: string) {
    const img = new Image();
    img.src = imageUrl;

    img.onload = () => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      if (ctx) {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);
        this.base64Image = canvas.toDataURL(); // Get Base64 string of the image
        console.log('Base64 Image:', this.base64Image); // For debugging
      }
    };
  }

  loadImages() {
      // Dynamically populate the images array based on sequential naming
      for (let i = 1; i <= 10; i++) {
          this.images.push({
              previewImageSrc: `images/group_images/picture${i}.jpg`,
              thumbnailImageSrc: `images/group_images/picture${i}.jpg`, // Optional thumbnail
              alt: `Picture ${i}`,
              title: `Picture ${i}`,
          });
      }
  }



  onSubmit() {
    if (this.groupForm.invalid || !this.base64Image) {
      alert('Please complete all required fields and select an image!');
      return;
    }

    const body = {
      name: this.groupForm.value.name,
      image: this.base64Image, // Attach the Base64 image
    };

    this.http.post<any>(this.apiUrl + '/groups/create', body).subscribe({
      next: (response) => {
        console.log('Group created successfully:', response);
        alert('Group created successfully!');

        if (response.id) {
          this.router.navigate(['/group', response.id]); // Navigate to the group's page
        } else {
          alert('Group ID not found in the response.');
        }
      },
      error: (error) => {
        console.error('Error creating group:', error);
        alert('Failed to create group.');
      },
    });

    // Reset the form and clear the image selection
    this.selectedImage = null; // Deselect the image
    this.groupForm.reset();
    this.base64Image = '';
  }

}
