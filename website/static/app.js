$(document).ready(function() {
    
    ////// DELETION //////
    $('.delete-college').click(function(event) {
        event.preventDefault();
        var collegeCode = $(this).data('college-code');

        if (confirm('Are you sure you want to delete this college?')) {
            // Send a DELETE request using AJAX
            $.ajax({
                type: 'DELETE',
                url: '/colleges/delete/' + collegeCode,
                success: function(data) {
                    if (data.success) {
                        // Remove the deleted row from the table
                        $(event.target).closest('tr').remove();
                        alert('College deleted successfully.');
                    } else {
                        alert('Failed to delete the college.');
                    }
                },
                error: function() {
                    alert('Failed to delete the college.');
                }
            });
        }
    });
    
    $('.delete-course').click(function(event) {
        event.preventDefault();
        var courseCode = $(this).data('course-code');

        if (confirm('Are you sure you want to delete this course?')) {
            // Send a DELETE request using AJAX
            $.ajax({
                type: 'DELETE',
                url: '/courses/delete/' + courseCode,
                success: function(data) {
                    if (data.success) {
                        // Remove the deleted row from the table
                        $(event.target).closest('tr').remove();
                        alert('Course deleted successfully.');
                    } else {
                        alert('Failed to delete the course.');
                    }
                },
                error: function() {
                    alert('Failed to delete the course.');
                }
            });
        }
    });

    $('.delete-student').click(function(event) {
        event.preventDefault();
        var studentId = $(this).data('student-id');

        if (confirm('Are you sure you want to delete this student?')) {
            // Send a DELETE request using AJAX
            $.ajax({
                type: 'DELETE',
                url: '/students/delete/' + studentId,
                success: function(data) {
                    if (data.success) {
                        // Remove the deleted row from the table
                        $(event.target).closest('tr').remove();
                        alert('Student deleted successfully.');
                    } else {
                        alert('Failed to delete the student.');
                    }
                },
                error: function() {
                    alert('Failed to delete the student.');
                }
            });
        }
    });

    ////// DELETION //////

    ////// SEARCH  //////


    $('#searchButton').on('click', function() {
        var searchQuery = $('#searchInput').val();
        window.location.href = "/colleges?search=" + searchQuery;
      });

      $('#searchButtonCourse').on('click', function() {
        var searchQueryCourse = $('#searchInputCourse').val();
        window.location.href = "/courses?search=" + searchQueryCourse;
    });
    
    $('#searchButtonStudents').on('click', function() {
        var searchQueryStudents = $('#searchInputStudents').val();
        window.location.href = "/students?search=" + searchQueryStudents;
    });
    
    ////// SEARCH //////


    /////// REFRESH BUTTON ///////
    function redirectToColleges() {
        window.location.href = '/colleges';
    }

    $('#refreshButton').on('click', function() {
        redirectToColleges();
    });

    function redirectToCourse() {
        window.location.href = '/courses';
    }

        // Event listener for the refresh button
    $('#refreshButtonCourse').on('click', function() {
        redirectToCourse();
    });

    function redirectToStudent() {
        window.location.href = '/students';
    }

        // Event listener for the refresh button
    $('#refreshButtonStudent').on('click', function() {
        redirectToStudent();
    });

    /////// REFRESH BUTTON ///////


    ////// TRANSFER DATA TO EDIT FORM //////

    // Listen for the "Edit" button click for colleges
    const editButtonsCollege = document.querySelectorAll('.edit-college');
    editButtonsCollege.forEach(button => {
        button.addEventListener('click', () => {
            const collegeCode = button.getAttribute('data-college-code');
            const collegeName = button.getAttribute('data-college-name');

            // Populate the edit form fields
            const editCollegeCodeField = document.getElementById('editCollegeCode');
            const editCollegeNameField = document.getElementById('editCollegeName');
            editCollegeCodeField.value = collegeCode;
            editCollegeNameField.value = collegeName;
        });
    });


    const editButtonsCourse = document.querySelectorAll('.edit-course');
    editButtonsCourse.forEach(button => {
        button.addEventListener('click', () => {
            const courseCode = button.getAttribute('data-course-code');
            const courseName = button.getAttribute('data-course-name');
            const collegeCode = button.getAttribute('data-college-code');

            // Populate the edit form fields
            const editCourseCodeField = document.getElementById('editCourseCode');
            const editCourseNameField = document.getElementById('editCourseName');
            const editCollegeCodeField = document.getElementById('editCollegeCode');
            editCourseCodeField.value = courseCode;
            editCourseNameField.value = courseName;
            editCollegeCodeField.value = collegeCode;
        });
    });

    const editButtonsStudent = document.querySelectorAll('.edit-student');
    editButtonsStudent.forEach(button => {
        button.addEventListener('click', () => {
            const studentID = button.getAttribute('data-student-id');
            const firstName = button.getAttribute('data-first-name');
            const lastName = button.getAttribute('data-last-name');
            const courseCode = button.getAttribute('data-course-code');
            const year = button.getAttribute('data-year');
            const gender = button.getAttribute('data-gender');

            // Populate the edit form fields
            const editStudentIDField = document.getElementById('editStudentID');
            const editFirstNameField = document.getElementById('editFirstName');
            const editLastNameField = document.getElementById('editLastName');
            const editCourseField = document.getElementById('editCourse');
            const editYearField = document.getElementById('editYear');
            const editGenderField = document.getElementById('editGender');

            editStudentIDField.value = studentID;
            editFirstNameField.value = firstName;
            editLastNameField.value = lastName;
            editCourseField.value = courseCode;
            editYearField.value = year;
            editGenderField.value = gender;
        });
    });

    const ProfileStudent = document.querySelectorAll('.view-student');

    ProfileStudent.forEach(button => {
        button.addEventListener('click', () => {
            const studentID = button.getAttribute('data-student-id-prof');
            const firstName = button.getAttribute('data-first-name-prof');
            const lastName = button.getAttribute('data-last-name-prof');
            const courseCode = button.getAttribute('data-course-code-prof');
            const collegeName = button.getAttribute('data-college-name-prof');
            const year = button.getAttribute('data-year-prof');
            const gender = button.getAttribute('data-gender-prof');
            const profilePicUrl = button.getAttribute('data-profile-pic-prof');

            // Populate the edit form fields
            const StudentIDField = document.getElementById('inputID');
            const FirstNameField = document.getElementById('inputFirstName');
            const LastNameField = document.getElementById('inputLastName');
            const CourseField = document.getElementById('inputCourse');
            const CollegeField = document.getElementById('inputCollege');
            const YearField = document.getElementById('inputYear');
            const GenderField = document.getElementById('inputGender');
            const ProfilePicField = document.getElementById(`img-source_${studentID}`); // Use the correct ID

            StudentIDField.value = studentID;
            FirstNameField.value = firstName;
            LastNameField.value = lastName;
            CourseField.value = courseCode;
            CollegeField.value = collegeName;
            YearField.value = year;
            GenderField.value = gender;

            console.log('profilePicUrl:', profilePicUrl);
            ProfilePicField.src = (profilePicUrl && profilePicUrl !== '' && profilePicUrl.toLowerCase() !== 'none') ? profilePicUrl : 'static/default-prof.png';
            console.log('Final src:', ProfilePicField.src);


        });
    });


    

    ////// TRANSFER DATA TO EDIT FORM //////

    ////// EDIT //////

    $(".edit-college").click(function () {
        var collegeCode = $(this).data("college-code");
        var collegeName = $(this).data("college-name");

        $("#editCollegeCode").val(collegeCode);
        $("#editCollegeName").val(collegeName);
    });

    $("#editCollegeForm").submit(function (e) {
        e.preventDefault();
        var collegeCode = $("#editCollegeCode").val();
        var newCollegeName = $("#editCollegeName").val();

        $.ajax({
            type: "POST",
            url: `/colleges/edit/${collegeCode}`,
            data: {
                collegeName: newCollegeName,
            },
            success: function (response) {
                if (response.success) {
                    alert("College updated successfully");
                    window.location.reload();
                } else {
                    alert("Failed to update college");
                }
            },
        });
    });

    $(".edit-course").click(function () {
        var courseCode = $(this).data("course-code");
        var courseName = $(this).data("course-name");
        var collegeCode = $(this).data("college-code");

        $("#editCourseCode").val(courseCode);
        $("#editCourseName").val(courseName);
        $("#editCollegeCode").val(collegeCode);
    });

    $("#editCourseForm").submit(function (e) {
        e.preventDefault();
        var courseCode = $("#editCourseCode").val();
        var newCourseName = $("#editCourseName").val();
        var collegeCode = $("#editCollegeCode").val(); 

        $.ajax({
            type: "POST",
            url: `/courses/edit/${courseCode}`,
            data: {
                courseName: newCourseName,
                collegeCode: collegeCode, 
            },
            success: function (response) {
                if (response.success) {
                    alert("Course updated successfully");
                    window.location.reload();
                } else {
                    alert("Failed to update course");
                }
            },
        });
    });

    $(".edit-student").click(function () {
        var studentId = $(this).data("student-id");
        var firstName = $(this).data("first-name");
        var lastName = $(this).data("last-name");
        var courseCode = $(this).data("course-code");
        var year = $(this).data("year");
        var gender = $(this).data("gender");
    
        $("#editStudentID").val(studentId);
        $("#editFirstName").val(firstName);
        $("#editLastName").val(lastName);
        $("#editCourseCode").val(courseCode);
        $("#editYear").val(year);
        $("#editGender").val(gender);
    });
    
    $("#editStudentForm").submit(function (e) {
        e.preventDefault();
        var studentId = $("#editStudentID").val();
        var newFirstName = $("#editFirstName").val();
        var newLastName = $("#editLastName").val();
        var newCourseCode = $("#editCourseCode").val();
        var newYear = $("#editYear").val();
        var newGender = $("#editGender").val();
    
        $.ajax({
            type: "POST",
            url: `/students/edit/${studentId}`,
            data: {
                firstName: newFirstName,
                lastName: newLastName,
                courseCode: newCourseCode,
                year: newYear,
                gender: newGender
            },
            success: function (response) {
                if (response.success) {
                    alert("Student updated successfully");
                    window.location.reload();
                } else {
                    alert("Failed to update student");
                }
            },
        });
    });
  });
    
  ////// EDIT //////

  ////// UPLOAD IMAGE //////

  var CLOUDINARY_URL = 'https://api.cloudinary.com/v1_1/dpydk3dsv/upload';
  var CLOUDINARY_UPLOAD_PRESET = 'cjxybr6b';
  
  var uploadProfilePicButtons = document.querySelectorAll('.profilePictureInput');
  var imgSources = document.querySelectorAll('.img-account-profile');
  
  uploadProfilePicButtons.forEach(function (uploadProfilePicButton) {
      uploadProfilePicButton.addEventListener('change', function (event) {
          var fileInput = event.currentTarget;
          var file = fileInput.files[0];
  
          var formData = new FormData();
          formData.append('file', file);
          formData.append('upload_preset', CLOUDINARY_UPLOAD_PRESET);
  
          var studentId = fileInput.getAttribute('data-student-id-prof');
  
          axios({
              url: CLOUDINARY_URL,
              method: 'POST',
              headers: {
                  'Content-Type': 'application/x-www-form-urlencoded'
              },
              data: formData
          }).then(function (res) {
              // Update the image source with the new URL
              var imgSource = document.querySelector('#img-source_' + studentId);
              if (imgSource) {
                  imgSource.src = res.data.secure_url;
              }
  
              // Send the studentId and secure_url to your server for database update
              axios.post('/update_profile_pic', { studentId: studentId, secureUrl: res.data.secure_url })
                  .then(function (response) {
                      // Display a success flash message
                      var flashMessage = response.data.message;
                      var modalHeader = document.querySelector('.small.font-italic.text-muted.mb-4');
                      var flashDiv = document.createElement('div');
                      flashDiv.className = 'alert alert-success';
                      flashDiv.innerHTML = flashMessage;
                      modalHeader.appendChild(flashDiv);
                  })
                  .catch(function (error) {
                      console.log(error);
                  });
          }).catch(function (err) {
              // Display an error flash message
              console.log(err);
              var flashMessage = 'Wrong file type or size is greater than 5MB';
              var modalHeader = document.querySelector('.small.font-italic.text-muted.mb-4');
              var flashDiv = document.createElement('div');
              flashDiv.className = 'alert alert-danger';
              flashDiv.innerHTML = flashMessage;
              modalHeader.appendChild(flashDiv);
          });
      });
  });
  

$('#studentProfileModal').on('show.bs.modal', function (event) {
    var modal = $(this);
    modal.find('form')[0].reset(); // Reset form fields
    modal.find('img.img-account-profile').attr('src', ''); // Clear profile picture
  });

    
  ////// UPLOAD IMAGE //////
  
  ///// FUNCTION FOR HIDING UPLOAD BUTTONS THAT AREN'T ASSOCIATED WITH THE STUDENT PROFILE //////
  const ProfileStudent = document.querySelectorAll('.view-student');
  ProfileStudent.forEach(button => {
    button.addEventListener('click', () => {
      const studentID = button.getAttribute('data-student-id-prof');

      // Hide all upload buttons and inputs initially
      const uploadButtons = document.querySelectorAll('.profileUploadBtn');
      const uploadInputs = document.querySelectorAll('.profilePictureInput');
      uploadButtons.forEach(uploadButton => {
        uploadButton.style.display = 'none';
      });
      uploadInputs.forEach(uploadInput => {
        uploadInput.style.display = 'none';
      });

      // Show the upload button and input associated with the clicked student
      const uploadButton = document.querySelector(`label[for="profilePicture_${studentID}"]`);
      const uploadInput = document.getElementById(`profilePicture_${studentID}`);

      if (uploadButton && uploadInput) {
        uploadButton.style.display = 'block';
        uploadInput.style.display = 'none';
      }
    });
  });