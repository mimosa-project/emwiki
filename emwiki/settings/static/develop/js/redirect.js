export default {
  mounted() {
    const checkbox = document.getElementById('redirectCheckbox');
    if (checkbox) {
    } else {
      window.location.href = 'https://github.dev/{{ github_id }}/{{ repository_url }}';
    }
  },
};
