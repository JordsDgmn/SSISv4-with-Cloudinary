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
    // Students table - SERVER-SIDE (backend handles filtering/sorting for scalability)
    if (document.getElementById('studentsTable')) {
      console.log('[STUDENTS] Initializing server-side DataTable...');
      
      // Store column filter values (will be sent to backend)
      window.studentColumnFilters = {
        studentId: '',
        name: '',
        program: '',
        year: '',
        gender: ''
      };
      
      const studentsTable = $('#studentsTable').DataTable({
        serverSide: true,
        processing: true,
        pageLength: 25,
        ajax: {
          url: '/students/data',
          type: 'POST',
          contentType: 'application/json',
          data: function(d) {
            // Add custom column filters to request
            d.columnFilters = window.studentColumnFilters;
            console.log('[STUDENTS] AJAX Request with filters:', d);
            return JSON.stringify(d);
          },
          dataSrc: function(json) {
            console.log('[STUDENTS] AJAX Response:', json);
            if (!json) {
              console.error('[STUDENTS] Empty response from server');
              SSISApp.showError('Empty response from server when loading students.');
              return [];
            }
            if (json.error) {
              console.error('[STUDENTS] Server error:', json.error);
              SSISApp.showError('Server error: ' + json.error);
              return [];
            }
            if (json.warnings && json.warnings.length) {
              console.warn('[STUDENTS] Warnings from server:', json.warnings);
              SSISApp.showWarning('Warnings: ' + json.warnings.join('; '));
            }
            return json.data || [];
          },
          beforeSend: function() {
            // Disable Apply filters button while request is in flight
            $('#applyFilters').prop('disabled', true).addClass('disabled');
            $('#applyFilters').append(' <span id="applySpinner" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
          },
          complete: function() {
            // Re-enable Apply filters button
            $('#applyFilters').prop('disabled', false).removeClass('disabled');
            $('#applySpinner').remove();
          },
          error: function(jqXHR, textStatus, errorThrown) {
            console.error('[STUDENTS] AJAX ERROR:', textStatus, errorThrown, jqXHR.responseText);
            SSISApp.showError('AJAX error loading students: ' + textStatus + ' ' + errorThrown);
            const debugDiv = document.getElementById('debug-log') || document.createElement('div');
            debugDiv.id = 'debug-log';
            debugDiv.style.cssText = 'position: fixed; bottom: 0; right: 0; background: #f00; color: #fff; font-family: monospace; font-size: 12px; padding: 15px; max-height: 300px; overflow-y: auto; max-width: 600px; border: 2px solid #f00; z-index: 9999;';
            debugDiv.innerHTML = '<strong style="color: yellow;">🚨 AJAX ERROR:</strong><br>' + 
              'Status: ' + textStatus + '<br>' +
              'Error: ' + errorThrown + '<br>' +
              'Code: ' + jqXHR.status + '<br>' +
              'Response: ' + (jqXHR.responseText ? jqXHR.responseText.substring(0, 1000) : '');
            if (!document.getElementById('debug-log')) document.body.appendChild(debugDiv);
          }
        },
        columnDefs: [
          { 
            targets: 0,
            data: 'profile_pic',
            orderable: false,
            render: function(data) {
              if (data) {
                return `<div class="profile-pic-container"><img src="${data}" alt="Profile" class="profile-pic" style="width: 40px; height: 40px; border-radius: 50%;"></div>`;
              }
              return '<div class="profile-pic-container"><i class="bi bi-person profile-placeholder"></i></div>';
            }
          },
          { targets: 1, data: 'id' },
          { 
            targets: 2, 
            data: null,
            render: function(data, type, row) {
              return (row.firstname || '') + ' ' + (row.lastname || '');
            }
          },
          { targets: 3, data: 'program_name', defaultContent: '<span class="text-muted">N/A</span>' },
          { targets: 4, data: 'college_name', defaultContent: '<span class="text-muted">N/A</span>' },
          { targets: 5, data: 'year' },
          { targets: 6, data: 'gender' },
          { 
            targets: 7,
            data: null,
            orderable: false,
            render: function(data, type, row) {
              const isAuthenticated = document.querySelector('[data-user-authenticated]') !== null;
              let buttons = `
                <div class="btn-group" role="group">
                  <a href="/students/view/${row.id}" class="btn btn-outline-info btn-sm" title="View Details">
                    <i class="bi bi-eye"></i>
                  </a>`;
              
              if (isAuthenticated) {
                buttons += `
                  <button type="button" class="btn btn-outline-primary btn-sm edit-student"
                    data-student-id="${row.id}"
                    data-student-firstname="${row.firstname}"
                    data-student-lastname="${row.lastname}"
                    data-student-program-id="${row.program_id || ''}"
                    data-student-year="${row.year}"
                    data-student-gender="${row.gender}"
                    data-bs-toggle="modal" data-bs-target="#editStudentModal" title="Edit Student">
                    <i class="bi bi-pencil"></i>
                  </button>
                  <a href="javascript:void(0)" class="btn btn-outline-danger btn-sm delete-student"
                    data-student-id="${row.id}"
                    data-student-firstname="${row.firstname}"
                    data-student-lastname="${row.lastname}" title="Delete Student">
                    <i class="bi bi-trash"></i>
                  </a>`;
              }
              
              buttons += `</div>`;
              return buttons;
            }
          }
        ],
        order: [[1, 'asc']],
        language: {
          search: "_INPUT_",
          searchPlaceholder: "Search records...",
          lengthMenu: "Show _MENU_ entries",
          info: "Showing _START_ to _END_ of _TOTAL_ entries",
          infoEmpty: "Showing 0 to 0 of 0 entries",
          infoFiltered: "(filtered from _MAX_ total entries)",
          zeroRecords: "No matching records found",
          emptyTable: "No data available in table",
          processing: "Loading..."
        },
        dom: '<"row mb-3"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>rtip'
      });
      
      console.log('[STUDENTS] ✅ Server-side DataTable initialized');
      
      // Store reference globally for filter handlers
      window.studentsTableInstance = studentsTable;

      // Listen for xhr events to report server-side diagnostics
      studentsTable.on('xhr', function(e, settings, json) {
        console.log('[STUDENTS] XHR event, response:', json);
        if (json && json.warnings) {
          SSISApp.showWarning('Server warnings: ' + json.warnings.join('; '));
        }
        if (json && json.error) {
          SSISApp.showError('Server error: ' + json.error);
        }

        // If filters were set but server didn't reduce the result set, warn user
        const filters = window.studentColumnFilters || {};
        const anyFilterSet = Object.values(filters).some(v => v !== null && String(v).trim() !== '');
        if (json && anyFilterSet && json.recordsFiltered === json.recordsTotal) {
          console.warn('[STUDENTS] Filters were applied but server returned unfiltered results');
          SSISApp.showWarning('Filters applied but server returned unfiltered results — check server logs/debug.');
          if (json.debug) {
            console.log('[STUDENTS] Server debug:', json.debug);
            // Show short debug message in UI for development
            SSISApp.showToast('Server debug: where=' + (json.debug.where_clause || 'none'), 'info');
          }
        }

        // If zero records after filtering, show info for user
        if (json && (json.recordsFiltered === 0)) {
          SSISApp.showToast('No matching records found for current filters.', 'info');
        }
      });
    }

    // Programs table - SERVER-SIDE PROCESSING
    if (document.getElementById('programsTable')) {
      const programsTable = $('#programsTable').DataTable({
        serverSide: true,
        processing: true,
        ajax: {
          url: '/programs/data',
          type: 'POST',
          contentType: 'application/json',
          data: function(d) {
            // attach column filters
            d.columnFilters = window.programColumnFilters || {};
            console.log('[DataTables AJAX REQUEST] /programs/data:', d);
            return JSON.stringify(d);
          },
          dataSrc: function(json) {
            console.log('[DataTables AJAX RESPONSE] /programs/data:', json);
            if (!json) {
              console.error('[ERROR] Empty response!', json);
              SSISApp.showError('Empty response from server when loading programs.');
              return [];
            }
            if (json.error) {
              console.error('[ERROR] Server error:', json.error);
              SSISApp.showError('Server error: ' + json.error);
              return [];
            }
            if (json.warnings && json.warnings.length) {
              console.warn('[WARN] Server warnings:', json.warnings);
              SSISApp.showWarning('Warnings: ' + json.warnings.join('; '));
            }

            // Heuristic: If filters were set but server returned unfiltered results, warn the user and show server debug if available
            const filters = window.programColumnFilters || {};
            const anyFilterSet = Object.values(filters).some(v => v !== null && String(v).trim() !== '');
            if (json && anyFilterSet && json.recordsFiltered === json.recordsTotal) {
              console.warn('[PROGRAMS] Filters were applied but server returned unfiltered results');
              SSISApp.showWarning('Filters applied but server returned unfiltered results — check server logs/debug.');
              if (json.debug) {
                console.log('[PROGRAMS] Server debug:', json.debug);
                SSISApp.showToast('Server debug: where=' + (json.debug.where_clause || 'none'), 'info');
              }
            }

            return json.data || [];
          },
          error: function(xhr, error, thrown) {
            console.error('[DataTables AJAX ERROR] /programs/data:', error, thrown);
            console.error('[ERROR RESPONSE]:', xhr.responseText);
            SSISApp.showError('Error loading program data: ' + xhr.status + ' ' + thrown);
          }
        }, 
        columns: [
          { data: 'code' },
          { data: 'name' },
          { 
            data: 'college_name',
            render: function(data, type, row) {
              return data || '<span class="text-muted">No College</span>';
            }
          },
          { 
            data: null,
            orderable: false,
            render: function(data, type, row) {
              const isAuthenticated = document.querySelector('[data-user-authenticated]') !== null;
              let buttons = `
                <div class="btn-group" role="group">
                  <a href="/programs/view/${row.program_id}" class="btn btn-outline-info btn-sm" title="View Programs">
                    <i class="bi bi-eye"></i>
                  </a>`;
              
              if (isAuthenticated) {
                buttons += `
                  <button type="button" class="btn btn-outline-primary btn-sm edit-program"
                    data-program-id="${row.program_id}"
                    data-program-code="${row.code}"
                    data-program-name="${row.name}"
                    data-college-id="${row.college_id || ''}"
                    data-bs-toggle="modal" data-bs-target="#editProgramModal" title="Edit Program">
                    <i class="bi bi-pencil"></i>
                  </button>
                  <a href="javascript:void(0)" class="btn btn-outline-danger btn-sm delete-program"
                    data-program-id="${row.program_id}"
                    data-program-code="${row.code}"
                    data-program-name="${row.name}" title="Delete Program">
                    <i class="bi bi-trash"></i>
                  </a>`;
              }
              
              buttons += '</div>';
              return buttons;
            }
          }
        ],
        pageLength: 25,
        lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
        language: {
          search: "_INPUT_",
          searchPlaceholder: "Search programs...",
          lengthMenu: "Show _MENU_ entries",
          info: "Showing _START_ to _END_ of _TOTAL_ programs",
          infoEmpty: "Showing 0 to 0 of 0 programs",
          infoFiltered: "(filtered from _MAX_ total programs)",
          zeroRecords: "No matching programs found",
          emptyTable: "No programs available",
          processing: "Loading programs..."
        },
        dom: '<"row mb-3"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>rtip',
        order: [[0, 'asc']]
      });
    }

    // Colleges table - SERVER-SIDE PROCESSING
    if (document.getElementById('collegesTable')) {
      $('#collegesTable').DataTable({
        serverSide: true,
        processing: true,
        ajax: {
          url: '/colleges/data',
          type: 'POST',
          contentType: 'application/json',
          data: function(d) {
            d.columnFilters = window.collegeColumnFilters || {};
            console.log('[DataTables AJAX REQUEST] /colleges/data:', d);
            return JSON.stringify(d);
          },
          dataSrc: function(json) {
            console.log('[DataTables AJAX RESPONSE] /colleges/data:', json);
            if (!json || !json.data) {
              console.error('[ERROR] Response missing data property!', json);
              return [];
            }

            // Heuristic: warn if filters were set in the UI but server returned unfiltered results
            const filters = window.collegeColumnFilters || {};
            const anyFilterSet = Object.values(filters).some(v => v !== null && String(v).trim() !== '');
            if (json && anyFilterSet && json.recordsFiltered === json.recordsTotal) {
              console.warn('[COLLEGES] Filters were applied but server returned unfiltered results');
              SSISApp.showWarning('Filters applied but server returned unfiltered results — check server logs/debug.');
              if (json.debug) {
                console.log('[COLLEGES] Server debug:', json.debug);
                SSISApp.showToast('Server debug: where=' + (json.debug.where_clause || 'none'), 'info');
              }
            }

            return json.data;  // Return ONLY the data array
          },
          error: function(xhr, error, thrown) {
            console.error('[DataTables AJAX ERROR] /colleges/data:', error, thrown);
            console.error('[ERROR RESPONSE]:', xhr.responseText);
            alert('Error loading college data: ' + xhr.status + ' ' + thrown);
          }
        },
        columns: [
          { data: 'code' },
          { data: 'name' },
          { 
            data: null,
            orderable: false,
            render: function(data, type, row) {
              const isAuthenticated = document.querySelector('[data-user-authenticated]') !== null;
              let buttons = `
                <div class="btn-group" role="group">
                  <a href="/colleges/view/${row.code}" class="btn btn-outline-info btn-sm" title="View College">
                    <i class="bi bi-eye"></i>
                  </a>`;
              
              if (isAuthenticated) {
                buttons += `
                  <button type="button" class="btn btn-outline-primary btn-sm edit-college"
                    data-college-id="${row.college_id}"
                    data-college-code="${row.code}"
                    data-college-name="${row.name}"
                    data-bs-toggle="modal" data-bs-target="#editCollegeModal" title="Edit College">
                    <i class="bi bi-pencil"></i>
                  </button>
                  <a href="javascript:void(0)" class="btn btn-outline-danger btn-sm delete-college"
                    data-college-id="${row.college_id}"
                    data-college-code="${row.code}"
                    data-college-name="${row.name}" title="Delete College">
                    <i class="bi bi-trash"></i>
                  </a>`;
              }
              
              buttons += '</div>';
              return buttons;
            }
          }
        ],
        pageLength: 25,
        lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
        language: {
          search: "_INPUT_",
          searchPlaceholder: "Search colleges...",
          lengthMenu: "Show _MENU_ entries",
          info: "Showing _START_ to _END_ of _TOTAL_ colleges",
          infoEmpty: "Showing 0 to 0 of 0 colleges",
          infoFiltered: "(filtered from _MAX_ total colleges)",
          zeroRecords: "No matching colleges found",
          emptyTable: "No colleges available",
          processing: "Loading colleges..."
        },
        dom: '<"row mb-3"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>rtip',
        order: [[0, 'asc']]
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

  showError(message) {
    console.error('[SSISApp] ERROR:', message);
    this.showToast(message, 'error');
  },

  showWarning(message) {
    console.warn('[SSISApp] WARNING:', message);
    this.showToast(message, 'info');
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
