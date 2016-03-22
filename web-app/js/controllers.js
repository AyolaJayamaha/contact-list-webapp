var contactApp = angular.module('contactApp', []);

contactApp.controller('ContactListCtrl', function($scope, $http) {

  /* Simple GET list of contacts
   simple-rest app need to run in port 5000 
   if not please change to running server port and server host
  */
  $http({
    method: 'GET',
    url: 'http://localhost:5000/'
  }).then(function successCallback(response) {
    $scope.contacts = response.data.contacts;
    // this callback will be called asynchronously
    // when the response is available
  }, function errorCallback(response) {
    console.log('error in connecting http://localhost:5000/');
    // called asynchronously if an error occurs
    // or server returns response with an error status.
  });
});