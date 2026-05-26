program platform_welfare
  implicit none

  real :: exposure_quality, cognitive_overload, privacy_sensitivity
  real :: data_extraction_intensity, friction, welfare
  integer :: clicked, consented

  clicked = 1
  consented = 1
  exposure_quality = 0.52
  cognitive_overload = 0.42
  privacy_sensitivity = 0.55
  data_extraction_intensity = 0.10
  friction = 0.18

  welfare = clicked * exposure_quality &
          - 0.30 * cognitive_overload &
          - 0.45 * privacy_sensitivity * data_extraction_intensity * consented &
          - 0.15 * friction

  print *, "Synthetic platform user welfare:", welfare
end program platform_welfare
