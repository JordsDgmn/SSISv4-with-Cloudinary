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
      dom: '<"d-flex justify-content-between align-items-center mb-3"<"d-flex align-items-center"f><"d-flex align-items-center"l>>rtip',
      columnDefs: [
        { orderable: false, targets: -1 } // Disable sorting on Actions column
      ],
      order: [[0, 'asc']], // Default sort by first column
      drawCallback: function() {
        // Re-bind event handlers after table redraw
        SSISApp.bindEventHandlers();
      }
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
    $(document).off('click', '.edit-student').on('click', '.edit-student', function() {
      const data = $(this).data();
      $('#editStudentId').val(data.studentId);
      $('#editStudentIdHidden').val(data.studentId);
      $('#editFirstName').val(data.firstName);
      $('#editLastName').val(data.lastName);
      $('#editProgramCode').val(data.programCode);
      $('#editYear').val(data.year);
      $('#editGender').val(data.gender);
      
      // Set form action
      $('#editStudentForm').attr('action', `/students/edit/${data.studentId}`);
    });
    
    // Handle student edit form submission with AJAX
    $('#editStudentForm').off('submit').on('submit', function(e) {
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
    $(document).off('click', '.delete-student').on('click', '.delete-student', function(e) {
      e.preventDefault();
      e.stopPropagation();
      
      // If the click was on the icon, get the parent button's data
      const $button = $(e.target).hasClass('delete-student') ? $(e.target) : $(e.target).closest('.delete-student');
      const studentId = $button.data('student-id');
      const studentName = $button.data('student-name');
      
      console.log('=== DELETE BUTTON CLICKED ===');
      console.log('Target element:', e.target.tagName, e.target.className);
      console.log('Button element:', $button[0]);
      console.log('Student ID:', studentId);
      console.log('Student Name:', studentName);
      
      if (!studentId) {
        console.error('❌ ERROR: Student ID is missing!');
        console.log('Button HTML:', $button[0].outerHTML);
        alert('ERROR: Student ID is missing!');
        return;
      }
      
      console.log('📋 Showing confirmation dialog...');
      if (confirm(`Are you sure you want to delete ${studentName} (ID: ${studentId})?\n\nThis action cannot be undone.`)) {
        console.log('✅ User confirmed deletion');
        const deleteUrl = `/students/delete/${studentId}`;
        console.log('🔄 Initiating DELETE request to:', deleteUrl);
        console.log('⏳ Redirecting... (server will handle the deletion)');
        
        try {
          window.location.href = deleteUrl;
        } catch (error) {
          console.error('❌ Error during redirect:', error);
          alert('Error: Could not redirect to delete page');
        }
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
    $(document).off('click', '.edit-program').on('click', '.edit-program', function() {
      const data = $(this).data();
      const programCode = data.programCode || data.courseCode;
      const programName = data.programName || data.courseName;
      const collegeCode = data.collegeCode;
      
      console.log('Edit program clicked:', { programCode, programName, collegeCode });
      
      // Populate form fields with current values
      $('#editProgramCode').val(programCode);
      $('#editProgramName').val(programName);
      $('#editCollegeCode').val(collegeCode);
      
      // Set form action
      $('#editProgramForm').attr('action', `/programs/edit/${programCode}`);
      
      // Store original code for validation
      $('#editProgramForm').data('original-code', programCode);
    });
    
    // Handle program edit form submission with AJAX
    $('#editProgramForm').off('submit').on('submit', function(e) {
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
    $(document).off('click', '.edit-course').on('click', '.edit-course', function() {
      const data = $(this).data();
      $('#editCourseCode').val(data.courseCode);
      $('#editCourseName').val(data.courseName);
      $('#editCollegeCode').val(data.collegeCode);
      
      // Set form action
      $('#editCourseForm').attr('action', `/courses/edit/${data.courseCode}`);
    });

    // Delete program/course
    $(document).off('click', '.delete-course, .delete-program').on('click', '.delete-course, .delete-program', function(e) {
      e.preventDefault();
      e.stopPropagation();
      
      // If the click was on the icon, get the parent button's data
      const $button = $(e.target).hasClass('delete-program') || $(e.target).hasClass('delete-course') 
        ? $(e.target) 
        : $(e.target).closest('.delete-program, .delete-course');
      
      const programCode = $button.data('program-code') || $button.data('course-code');
      const programName = $button.data('program-name') || $button.data('course-name');
      
      console.log('='.repeat(80));
      console.log('🗑️  DELETE PROGRAM BUTTON CLICKED');
      console.log('='.repeat(80));
      console.log('Target element:', e.target.tagName, e.target.className);
      console.log('Button element:', $button[0]);
      console.log('Program Code:', programCode);
      console.log('Program Name:', programName);
      
      if (!programCode) {
        console.error('❌ ERROR: Program code is missing!');
        console.log('Button HTML:', $button[0].outerHTML);
        alert('ERROR: Program code is missing!');
        return;
      }
      
      console.log('📋 Showing confirmation dialog...');
      if (confirm(`Are you sure you want to delete program ${programName} (${programCode})?\n\nThis action cannot be undone.`)) {
        console.log('✅ User confirmed deletion');
        const deleteUrl = `/programs/delete/${programCode}`;
        console.log('🔄 Initiating DELETE request to:', deleteUrl);
        console.log('⏳ Redirecting... (server will handle the deletion)');
        console.log('='.repeat(80));
        
        try {
          window.location.href = deleteUrl;
        } catch (error) {
          console.error('❌ Error during redirect:', error);
          alert('Error: Could not redirect to delete page');
        }
      } else {
        console.log('❌ User cancelled deletion');
        console.log('='.repeat(80));
      }
    });
    
    console.log('Program handlers bound. Delete buttons found:', $('.delete-program, .delete-course').length);
  },

  // College-specific event handlers
  bindCollegeHandlers() {
    console.log('Binding college handlers...');
    
    // Edit college
    $(document).off('click', '.edit-college').on('click', '.edit-college', function() {
      const data = $(this).data();
      const collegeCode = data.collegeCode;
      const collegeName = data.collegeName;
      
      console.log('Edit college clicked:', { collegeCode, collegeName });
      
      // Populate form fields with current values
      $('#editCollegeCode').val(collegeCode);
      $('#editCollegeName').val(collegeName);
      
      // Set form action
      $('#editCollegeForm').attr('action', `/colleges/edit/${collegeCode}`);
      
      // Store original code for validation
      $('#editCollegeForm').data('original-code', collegeCode);
    });
    
    // Handle college edit form submission with AJAX
    $('#editCollegeForm').off('submit').on('submit', function(e) {
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
    $(document).off('click', '.delete-college').on('click', '.delete-college', function(e) {
      e.preventDefault();
      e.stopPropagation();
      
      // If the click was on the icon, get the parent button's data
      const $button = $(e.target).hasClass('delete-college') ? $(e.target) : $(e.target).closest('.delete-college');
      const collegeCode = $button.data('college-code');
      const collegeName = $button.data('college-name');
      
      console.log('='.repeat(80));
      console.log('🗑️  DELETE COLLEGE BUTTON CLICKED');
      console.log('='.repeat(80));
      console.log('Target element:', e.target.tagName, e.target.className);
      console.log('Button element:', $button[0]);
      console.log('College Code:', collegeCode);
      console.log('College Name:', collegeName);
      
      if (!collegeCode) {
        console.error('❌ ERROR: College code is missing!');
        console.log('Button HTML:', $button[0].outerHTML);
        alert('ERROR: College code is missing!');
        return;
      }
      
      console.log('📋 Showing confirmation dialog...');
      if (confirm(`Are you sure you want to delete college ${collegeName} (${collegeCode})?\n\nThis action cannot be undone.`)) {
        console.log('✅ User confirmed deletion');
        const deleteUrl = `/colleges/delete/${collegeCode}`;
        console.log('🔄 Initiating DELETE request to:', deleteUrl);
        console.log('⏳ Redirecting... (server will handle the deletion)');
        console.log('='.repeat(80));
        
        try {
          window.location.href = deleteUrl;
        } catch (error) {
          console.error('❌ Error during redirect:', error);
          alert('Error: Could not redirect to delete page');
        }
      } else {
        console.log('❌ User cancelled deletion');
        console.log('='.repeat(80));
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
      
      if (!$field[0].checkValidity() || $field.val().trim() === '') {
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
      
      // Check all required fields
      $(form).find('input[required], select[required], textarea[required]').each(function() {
        const $field = $(this);
        const value = $field.val();
        
        if (!value || value.trim() === '') {
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

  // Image upload preview
  previewImage(input) {
    if (input.files && input.files[0]) {
      const reader = new FileReader();
      reader.onload = function(e) {
        const preview = $(input).siblings('.image-preview');
        if (preview.length === 0) {
          $(input).after(`<div class="image-preview mt-2">
            <img src="${e.target.result}" class="img-thumbnail" style="max-width: 200px; max-height: 200px;">
          </div>`);
        } else {
          preview.find('img').attr('src', e.target.result);
        }
      };
      reader.readAsDataURL(input.files[0]);
    }
  }
};

// File input change handler for image preview
$(document).on('change', 'input[type="file"][accept*="image"]', function() {
  SSISApp.previewImage(this);
});

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM loaded, initializing SSISApp...');
  SSISApp.init();
});

// Export for global access
window.SSISApp = SSISApp;
