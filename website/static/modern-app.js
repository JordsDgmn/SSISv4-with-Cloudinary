// Modern SSIS Application JavaScript
// Version: 2.0 - Fixed delete button functionality
const SSISApp = {
  // Configuration
  config: {
    dataTableConfig: {
      responsive: true,
      pageLength: 25,
      lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
      language: {
        search: "_INPUT_",
        searchPlaceholder: "Search records...",
        lengthMenu: "Show _MENU_ entries",
        info: "Showing _START_ to _END_ of _TOTAL_ entries",
        infoEmpty: "Showing 0 to 0 of 0 entries",
        infoFiltered: "(filtered from _MAX_ total entries)",
        zeroRecords: "No matching records found",
        emptyTable: "No data available in table"
      },
      dom: '<"row mb-3"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>rtip',
      columnDefs: [
        { orderable: false, targets: -1 } // Disable sorting on Actions column
      ],
      order: [[0, 'asc']] // Default sort by first column
      // drawCallback removed - handlers use event delegation and don't need rebinding
    }
  },

  // Initialize application
  init() {
    console.log('SSISApp initializing...');
    // Dark mode is now handled in head script
    this.initDataTables();
    this.bindEventHandlers();
    this.initFormValidation();
    this.showWelcomeMessage();
    this.checkUrlForMessages(); // Check for success/error messages in URL
    console.log('SSISApp initialized successfully');
  },

  // Initialize DataTables for all pages
  initDataTables() {
    // Students table
    if (document.getElementById('studentsTable')) {
      $('#studentsTable').DataTable({
        ...this.config.dataTableConfig,
        order: [[0, 'asc']], // Sort by Student ID
        columnDefs: [
          { orderable: false, targets: -1 }, // Actions column
          { className: "text-center", targets: -1 }, // Center align Actions
          { width: "150px", targets: -1 } // Fixed width for actions
        ]
      });
    }

    // Programs table
    if (document.getElementById('programsTable')) {
      $('#programsTable').DataTable({
        ...this.config.dataTableConfig,
        order: [[0, 'asc']], // Sort by Program Code
        columnDefs: [
          { orderable: false, targets: -1 }, // Actions column
          { className: "text-center", targets: -1 }, // Center align actions
          { width: "150px", targets: -1 } // Fixed width for actions
        ]
      });
    }

    // Colleges table
    if (document.getElementById('collegesTable')) {
      $('#collegesTable').DataTable({
        ...this.config.dataTableConfig,
        order: [[0, 'asc']], // Sort by College Code
        columnDefs: [
          { orderable: false, targets: -1 }, // Actions column
          { className: "text-center", targets: -1 }, // Center align actions
          { width: "150px", targets: -1 } // Fixed width for actions
        ]
      });
    }
  },

  // Bind event handlers
  bindEventHandlers() {
    // Student form handlers
    this.bindStudentHandlers();
    
    // Course form handlers
    this.bindCourseHandlers();
    
    // College form handlers
    this.bindCollegeHandlers();
    
    // Global handlers
    this.bindGlobalHandlers();
  },

  // Student-specific event handlers
  bindStudentHandlers() {
    console.log('Binding student handlers...');
    
    // Edit student - use event delegation on document
    $(document).on('click', '.edit-student', function() {
      const data = $(this).data();
      console.log('Edit student clicked, data:', data);
      
      // Pre-fill ALL fields with existing data
      $('#editStudentId').val(data.studentId || '');
      $('#editStudentIdHidden').val(data.studentId || '');
      $('#editFirstName').val(data.firstName || '');
      $('#editLastName').val(data.lastName || '');
      $('#editProgramId').val(data.programId || '');  // Use program ID
      $('#editYear').val(data.year || '1st Year');
      $('#editGender').val(data.gender || '');
      
      // Handle profile picture
      if (data.profilePic) {
        $('#editCurrentProfile').show();
        $('#editCurrentProfileImg').attr('src', data.profilePic);
      } else {
        $('#editCurrentProfile').hide();
      }
      // Clear file input and remove checkbox
      $('#editProfilePic').val('');
      $('#editRemoveProfilePic').prop('checked', false);
      
      console.log('✅ All fields pre-filled:', {
        id: data.studentId,
        firstName: data.firstName,
        lastName: data.lastName,
        programId: data.programId,
        year: data.year,
        gender: data.gender
      });
      
      // Set form action
      $('#editStudentForm').attr('action', `/students/edit/${data.studentId}`);
    });
    
    // Handle student edit form submission with AJAX
    $('#editStudentForm').on('submit', function(e) {
      e.preventDefault();
      
      const form = $(this);
      const formData = new FormData(this);
      const submitBtn = form.find('button[type="submit"]');
      const originalBtnText = submitBtn.html();
      
      // Disable button and show loading
      submitBtn.prop('disabled', true).html('<i class="bi bi-arrow-clockwise me-2 spin"></i>Updating...');
      
      $.ajax({
        url: form.attr('action'),
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
          console.log('Student update response:', response);
          
          if (response.success) {
            // Close modal
            $('#editStudentModal').modal('hide');
            
            // Show success message and reload
            setTimeout(function() {
              window.location.href = '/students?success=' + encodeURIComponent(response.message || 'Student updated successfully');
            }, 300);
          } else {
            alert('Error: ' + (response.message || 'Failed to update student'));
            submitBtn.prop('disabled', false).html(originalBtnText);
          }
        },
        error: function(xhr, status, error) {
          console.error('Student update error:', error);
          alert('Error updating student: ' + error);
          submitBtn.prop('disabled', false).html(originalBtnText);
        }
      });
    });

    // Delete student - use event delegation on document
    $(document).on('click', '.delete-student', function(e) {
      e.preventDefault();
      e.stopPropagation();
      
      // Get data from the button
      const studentId = $(this).data('student-id');
      const studentName = $(this).data('student-name');
      
      console.log('=== DELETE BUTTON CLICKED ===');
      console.log('Student ID:', studentId);
      console.log('Student Name:', studentName);
      
      if (!studentId) {
        console.error('❌ ERROR: Student ID is missing!');
        alert('ERROR: Student ID is missing!');
        return;
      }
      
      if (confirm(`Are you sure you want to delete ${studentName} (ID: ${studentId})?\n\nThis action cannot be undone.`)) {
        console.log('✅ User confirmed deletion');
        const deleteUrl = `/students/delete/${studentId}`;
        console.log('🔄 Redirecting to:', deleteUrl);
        window.location.href = deleteUrl;
      } else {
        console.log('❌ User cancelled deletion');
      }
    });
    
    console.log('Student handlers bound. Delete buttons found:', $('.delete-student').length);
    
    // Add a test function to the window for debugging
    window.testDeleteClick = function() {
      console.log('\n' + '='.repeat(80));
      console.log('🧪 MANUAL TEST FUNCTION');
      console.log('='.repeat(80));
      console.log('Delete buttons found:', $('.delete-student').length);
      $('.delete-student').each(function(index) {
        console.log(`\n📋 Button ${index + 1}:`, {
          html: this.outerHTML.substring(0, 100) + '...',
          classes: this.className,
          studentId: $(this).data('student-id'),
          studentName: $(this).data('student-name'),
          visible: $(this).is(':visible'),
          offset: $(this).offset(),
          dimensions: { width: $(this).width(), height: $(this).height() }
        });
      });
      console.log('\n🔄 Attempting programmatic click on first button...');
      $('.delete-student').first().trigger('click');
      console.log('='.repeat(80) + '\n');
    };
    
    console.log('✅ Test function added. Run testDeleteClick() in console to debug.');
  },

  // Course-specific event handlers
  bindCourseHandlers() {
    console.log('Binding program/course handlers...');
    
    // Edit program
    $(document).on('click', '.edit-program', function() {
      const data = $(this).data();
      const programId = data.programId;
      const programCode = data.programCode || data.courseCode;
      const programName = data.programName || data.courseName;
      const collegeId = data.collegeId;
      
      console.log('Edit program clicked:', { programId, programCode, programName, collegeId });
      
      // Populate form fields with current values
      $('#editProgramCode').val(programCode);
      $('#editProgramName').val(programName);
      $('#editCollegeCode').val(collegeId);
      
      // Set form action
      $('#editProgramForm').attr('action', `/programs/edit/${programId}`);
      
      // Store original code for validation
      $('#editProgramForm').data('original-code', programCode);
    });
    
    // Handle program edit form submission with AJAX
    $('#editProgramForm').on('submit', function(e) {
      e.preventDefault();
      
      const form = $(this);
      const formData = new FormData(this);
      const submitBtn = form.find('button[type="submit"]');
      const originalBtnText = submitBtn.html();
      
      // Disable button and show loading
      submitBtn.prop('disabled', true).html('<i class="bi bi-arrow-clockwise me-2 spin"></i>Updating...');
      
      $.ajax({
        url: form.attr('action'),
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
          console.log('Program update response:', response);
          
          if (response.success) {
            // Close modal
            $('#editProgramModal').modal('hide');
            
            // Show success message and reload
            setTimeout(function() {
              window.location.href = '/programs?success=' + encodeURIComponent(response.message || 'Program updated successfully');
            }, 300);
          } else {
            alert('Error: ' + (response.message || 'Failed to update program'));
            submitBtn.prop('disabled', false).html(originalBtnText);
          }
        },
        error: function(xhr, status, error) {
          console.error('Program update error:', error);
          alert('Error updating program: ' + error);
          submitBtn.prop('disabled', false).html(originalBtnText);
        }
      });
    });
    
    // Edit course (legacy support)
    $(document).on('click', '.edit-course', function() {
      const data = $(this).data();
      $('#editProgramId').val(data.programId);
      $('#editCourseCode').val(data.courseCode);
      $('#editCourseName').val(data.courseName);
      $('#editCollegeCode').val(data.collegeId || '');
      
      // Set form action
      $('#editCourseForm').attr('action', `/courses/edit/${data.programId}`);
    });

    // Delete program/course
    $(document).on('click', '.delete-course, .delete-program', function(e) {
      e.preventDefault();
      e.stopPropagation();
      
      const programId = $(this).data('program-id');
      const programCode = $(this).data('program-code') || $(this).data('course-code');
      const programName = $(this).data('program-name') || $(this).data('course-name');
      
      console.log('=== DELETE PROGRAM CLICKED ===');
      console.log('Program ID:', programId);
      console.log('Program Code:', programCode);
      console.log('Program Name:', programName);
      
      if (!programId) {
        console.error('❌ ERROR: Program ID is missing!');
        alert('ERROR: Program ID is missing!');
        return;
      }
      
      if (confirm(`Are you sure you want to delete program ${programName} (${programCode})?\n\nStudents in this program will become orphaned.\nThis action cannot be undone.`)) {
        console.log('✅ User confirmed deletion');
        const deleteUrl = `/programs/delete/${programId}`;
        console.log('🔄 Redirecting to:', deleteUrl);
        window.location.href = deleteUrl;
      } else {
        console.log('❌ User cancelled deletion');
      }
    });
    
    console.log('Program handlers bound. Delete buttons found:', $('.delete-program, .delete-course').length);
  },

  // College-specific event handlers
  bindCollegeHandlers() {
    console.log('Binding college handlers...');
    
    // Edit college
    $(document).on('click', '.edit-college', function() {
      const data = $(this).data();
      const collegeId = data.collegeId;
      const collegeCode = data.collegeCode;
      const collegeName = data.collegeName;
      
      console.log('Edit college clicked:', { collegeId, collegeCode, collegeName });
      
      // Populate form fields with current values
      $('#editCollegeId').val(collegeId);
      $('#editCollegeCode').val(collegeCode);
      $('#editCollegeName').val(collegeName);
      
      // Set form action
      $('#editCollegeForm').attr('action', `/colleges/edit/${collegeId}`);
      
      // Store original code for validation
      $('#editCollegeForm').data('original-code', collegeCode);
    });
    
    // Handle college edit form submission with AJAX
    $('#editCollegeForm').on('submit', function(e) {
      e.preventDefault();
      
      const form = $(this);
      const formData = new FormData(this);
      const submitBtn = form.find('button[type="submit"]');
      const originalBtnText = submitBtn.html();
      
      // Disable button and show loading
      submitBtn.prop('disabled', true).html('<i class="bi bi-arrow-clockwise me-2 spin"></i>Updating...');
      
      $.ajax({
        url: form.attr('action'),
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
          console.log('College update response:', response);
          
          if (response.success) {
            // Close modal
            $('#editCollegeModal').modal('hide');
            
            // Show success message and reload
            setTimeout(function() {
              window.location.href = '/colleges?success=' + encodeURIComponent(response.message || 'College updated successfully');
            }, 300);
          } else {
            alert('Error: ' + (response.message || 'Failed to update college'));
            submitBtn.prop('disabled', false).html(originalBtnText);
          }
        },
        error: function(xhr, status, error) {
          console.error('College update error:', error);
          alert('Error updating college: ' + error);
          submitBtn.prop('disabled', false).html(originalBtnText);
        }
      });
    });

    // Delete college
    $(document).on('click', '.delete-college', function(e) {
      e.preventDefault();
      e.stopPropagation();
      
      const collegeId = $(this).data('college-id');
      const collegeCode = $(this).data('college-code');
      const collegeName = $(this).data('college-name');
      
      console.log('=== DELETE COLLEGE CLICKED ===');
      console.log('College ID:', collegeId);
      console.log('College Code:', collegeCode);
      console.log('College Name:', collegeName);
      
      if (!collegeId) {
        console.error('❌ ERROR: College ID is missing!');
        alert('ERROR: College ID is missing!');
        return;
      }
      
      if (confirm(`Are you sure you want to delete college ${collegeName} (${collegeCode})?\n\nPrograms in this college will become orphaned.\nThis action cannot be undone.`)) {
        console.log('✅ User confirmed deletion');
        const deleteUrl = `/colleges/delete/${collegeId}`;
        console.log('🔄 Redirecting to:', deleteUrl);
        window.location.href = deleteUrl;
      } else {
        console.log('❌ User cancelled deletion');
      }
    });
    
    console.log('College handlers bound. Delete buttons found:', $('.delete-college').length);
  },

  // Global event handlers
  bindGlobalHandlers() {
    // Form submission with loading states
    $('form').on('submit', function() {
      const submitBtn = $(this).find('button[type="submit"]');
      const originalText = submitBtn.html();
      
      submitBtn.prop('disabled', true)
             .html('<i class="bi bi-arrow-clockwise me-2 spin"></i>Processing...');
      
      // Re-enable after 3 seconds as fallback
      setTimeout(() => {
        submitBtn.prop('disabled', false).html(originalText);
      }, 3000);
    });

    // Auto-dismiss alerts
    setTimeout(() => {
      $('.alert-dismissible').fadeOut('slow');
    }, 5000);
  },

  // Form validation
  initFormValidation() {
    // Add real-time validation feedback
    $('input[required], select[required], textarea[required]').on('blur change', function() {
      const $field = $(this);
      const $formGroup = $field.closest('.form-floating, .mb-3');
      const value = $field.val();
      
      if (!$field[0].checkValidity() || (value !== null && value.trim() === '')) {
        $field.addClass('is-invalid');
        $field.removeClass('is-valid');
        
        // Add error icon if not exists
        if (!$formGroup.find('.invalid-feedback').length) {
          $formGroup.append('<div class="invalid-feedback d-flex align-items-center"><i class="bi bi-exclamation-circle me-2"></i>This field is required</div>');
        }
      } else {
        $field.removeClass('is-invalid');
        $field.addClass('is-valid');
        $formGroup.find('.invalid-feedback').remove();
      }
    });
    
    // Prevent form submission if any required fields are empty
    $('form').on('submit', function(e) {
      const form = this;
      let hasEmptyFields = false;
      
      // Check all required fields (not optional ones)
      $(form).find('input[required], select[required], textarea[required]').each(function() {
        const $field = $(this);
        const value = $field.val();
        
        // Only validate if field is truly required and value is empty
        if (!value || (typeof value === 'string' && value.trim() === '')) {
          hasEmptyFields = true;
          $field.addClass('is-invalid');
          $field.removeClass('is-valid');
          
          const $formGroup = $field.closest('.form-floating, .mb-3');
          if (!$formGroup.find('.invalid-feedback').length) {
            $formGroup.append('<div class="invalid-feedback d-flex align-items-center"><i class="bi bi-exclamation-circle me-2"></i>This field is required</div>');
          }
        }
      });
      
      if (hasEmptyFields) {
        e.preventDefault();
        e.stopPropagation();
        
        // Show alert
        const alertHtml = `
          <div class="alert alert-danger alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3" style="z-index: 9999;" role="alert">
            <i class="bi bi-exclamation-triangle me-2"></i>
            <strong>All fields are required!</strong> Please fill in all required fields before submitting.
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
          </div>
        `;
        
        // Remove existing alert if any
        $('.alert.position-fixed').remove();
        $('body').append(alertHtml);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
          $('.alert.position-fixed').fadeOut('slow', function() { $(this).remove(); });
        }, 5000);
        
        // Focus on first invalid field
        const firstInvalid = $(form).find('.is-invalid').first();
        firstInvalid.focus();
        
        return false;
      }
      
      $(form).addClass('was-validated');
    });
    
    // Clear validation on modal close
    $('.modal').on('hidden.bs.modal', function() {
      $(this).find('form').removeClass('was-validated');
      $(this).find('.is-invalid, .is-valid').removeClass('is-invalid is-valid');
      $(this).find('.invalid-feedback').remove();
    });
  },

  // Utility functions
  refreshTable(tableId) {
    if ($.fn.DataTable.isDataTable(`#${tableId}`)) {
      $(`#${tableId}`).DataTable().ajax.reload(null, false);
    } else {
      location.reload();
    }
  },

  showToast(message, type = 'info') {
    const alertClass = type === 'error' ? 'alert-danger' : 
                      type === 'success' ? 'alert-success' : 
                      'alert-info';
    
    const toast = $(`
      <div class="alert ${alertClass} alert-dismissible fade show position-fixed" 
           style="top: 20px; right: 20px; z-index: 9999; min-width: 300px;" role="alert">
        <i class="bi bi-${type === 'error' ? 'exclamation-triangle' : 
                          type === 'success' ? 'check-circle' : 
                          'info-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      </div>
    `);
    
    $('body').append(toast);
    
    // Auto-dismiss after 4 seconds
    setTimeout(() => {
      toast.fadeOut('slow', () => toast.remove());
    }, 4000);
  },

  showWelcomeMessage() {
    // Show welcome message for first-time visitors
    if (!localStorage.getItem('ssis_visited')) {
      setTimeout(() => {
        this.showToast('Welcome to the Modern Student Information System!', 'success');
        localStorage.setItem('ssis_visited', 'true');
      }, 1000);
    }
  },

  // Check URL for success/error messages (from redirects after CRUD operations)
  checkUrlForMessages() {
    const urlParams = new URLSearchParams(window.location.search);
    const successMsg = urlParams.get('success');
    const errorMsg = urlParams.get('error');
    
    if (successMsg) {
      this.showAlert(decodeURIComponent(successMsg), 'success');
      // Remove the parameter from URL without reloading
      const newUrl = window.location.pathname;
      window.history.replaceState({}, document.title, newUrl);
    }
    
    if (errorMsg) {
      this.showAlert(decodeURIComponent(errorMsg), 'error');
      // Remove the parameter from URL without reloading
      const newUrl = window.location.pathname;
      window.history.replaceState({}, document.title, newUrl);
    }
  },

  // Show alert message in the flash container
  showAlert(message, type = 'success') {
    const alertClass = type === 'error' || type === 'danger' ? 'alert-danger' : 'alert-success';
    const iconClass = type === 'error' || type === 'danger' ? 'exclamation-triangle' : 'check-circle';
    
    const alertHtml = `
      <div class="alert ${alertClass} alert-dismissible fade show shadow-sm" role="alert">
        <i class="bi bi-${iconClass} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      </div>
    `;
    
    $('#js-message-container').html(alertHtml);
    
    // Auto-dismiss after 8 seconds
    setTimeout(() => {
      $('#js-message-container .alert').fadeOut('slow', function() { $(this).remove(); });
    }, 8000);
  },

  // Image upload validation and preview
  validateAndPreviewImage(input) {
    const file = input.files[0];
    const $input = $(input);
    const $errorDiv = $input.siblings('.invalid-feedback');
    const $preview = $input.siblings('.image-preview');
    
    // Clear previous errors and preview
    $input.removeClass('is-invalid');
    $errorDiv.hide().text('');
    $preview.remove();
    
    if (!file) {
      return true; // No file selected is OK (optional field)
    }
    
    // Validate file type (PNG and JPEG only)
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg'];
    const fileExtension = file.name.split('.').pop().toLowerCase();
    const allowedExtensions = ['png', 'jpg', 'jpeg'];
    
    if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
      $input.addClass('is-invalid');
      $errorDiv.html(`
        <i class="bi bi-exclamation-circle me-1"></i>
        <strong>Invalid file type!</strong> Only PNG and JPEG images are allowed.
      `).show();
      $input.val(''); // Clear the invalid file
      return false;
    }
    
    // Validate file size (2MB = 2097152 bytes)
    const maxSizeBytes = 2 * 1024 * 1024; // 2MB in bytes
    const fileSizeKB = (file.size / 1024).toFixed(2);
    const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
    
    if (file.size > maxSizeBytes) {
      $input.addClass('is-invalid');
      $errorDiv.html(`
        <i class="bi bi-exclamation-circle me-1"></i>
        <strong>File too large!</strong> Your file is ${fileSizeMB}MB (${fileSizeKB}KB). Maximum allowed size is 2MB (2048KB).
      `).show();
      $input.val(''); // Clear the invalid file
      return false;
    }
    
    // File is valid - show success state and preview
    $input.addClass('is-valid');
    
    // Show preview
    const reader = new FileReader();
    reader.onload = function(e) {
      $input.after(`
        <div class="image-preview mt-2 alert alert-success p-2">
          <div class="d-flex align-items-center gap-2">
            <img src="${e.target.result}" class="img-thumbnail" style="max-width: 120px; max-height: 120px; object-fit: cover;">
            <div class="flex-grow-1">
              <div class="mb-1" style="color: #000;">
                <i class="bi bi-check-circle me-1"></i><strong>Valid image</strong>
              </div>
              <small class="d-block" style="color: #000; opacity: 0.8;">${file.name}</small>
              <small class="d-block" style="color: #000; opacity: 0.8;">${fileSizeKB}KB (${fileSizeMB}MB)</small>
            </div>
          </div>
        </div>
      `);
    };
    reader.readAsDataURL(file);
    
    return true;
  }
};

// File input change handler with validation
$(document).on('change', 'input[type="file"][accept*="image"]', function() {
  SSISApp.validateAndPreviewImage(this);
});

// Also validate on form submission as a final check
$(document).on('submit', 'form:has(input[type="file"][accept*="image"])', function(e) {
  const $fileInputs = $(this).find('input[type="file"][accept*="image"]');
  let allValid = true;
  
  $fileInputs.each(function() {
    if (this.files.length > 0) {
      if (!SSISApp.validateAndPreviewImage(this)) {
        allValid = false;
      }
    }
  });
  
  if (!allValid) {
    e.preventDefault();
    e.stopPropagation();
    
    // Scroll to first error
    const $firstError = $('.is-invalid').first();
    if ($firstError.length) {
      $firstError[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
      $firstError.focus();
    }
    
    return false;
  }
});

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM loaded, initializing SSISApp...');
  SSISApp.init();
});

// Export for global access
window.SSISApp = SSISApp;
