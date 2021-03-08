import { ref } from "vue";
export const userInfo = ref({
  email: "",
  password: "",
});
export const rules = ref({
  name: [
    {
      required: true,
      trigger: "blur",
    },
  ],
  email: [
    {
      type: "email",
      required: true,
      trigger: "blur",
    },
  ],
  password: [
    {
      required: true,
      message: "Password could not be empty...",
      trigger: "blur",
    },
    {
      min: 6,
      max: 30,
      message: "Password's length has to be 6 to 30 characters...",
      trigger: "blur",
    },
  ],
});

export const RegisterInfo = ref({
  name: "",
  email: "",
  password: "",
});
